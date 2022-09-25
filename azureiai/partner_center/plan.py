import json
from distutils.util import strtobool
from pathlib import Path

import yaml
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer

from azureiai.managed_apps.confs.variant import OfferListing, FeatureAvailability, Package
from azureiai.partner_center import CLIParser
from azureiai.partner_center.submission import Submission
from swagger_client.rest import ApiException

AZURE_APPLICATION = "AzureApplication"


class Plan(Submission):
    """Azure Partner Center Managed Application Submission"""

    def __init__(
        self,
        plan_name=None,
        name=None,
        config_yaml=r"config.yml",
        app_path: str = ".",
        json_listing_config="ma_config.json",
        subtype="",
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_APPLICATION,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )
        self.plan_name = plan_name
        self.subtype = subtype

    def create(self):
        """
        Create new AMA Plan and retry up to 5 times.

        return: variant post api response
        """
        body = {
            "resourceType": "AzureSkuVariant",
            "state": "Active",
            "friendlyName": self.plan_name.replace("-", " "),
            "leadGenID": "publisher_name." + self.plan_name,
            "externalID": self.plan_name,
            "cloudAvailabilities": ["public-azure"],
        }
        if self.subtype == "ma":
            body["SubType"] = "managed-application"
        elif self.subtype == "st":
            body["SubType"] = "solution-template"

        if not self._ids["product_id"]:
            self._set_product_id()

        api_response = self._apis["variant"].products_product_id_variants_post(
            authorization=self.get_auth(),
            product_id=self._ids["product_id"],
            body=body,
        )
        self._ids["plan_id"] = api_response["id"]
        self.update()
        return api_response

    def update(self):
        """Update Existing Application"""
        if not self._ids["product_id"]:
            self.show()

        self._update_plan_listing()
        self._update_pricing_and_availability()
        self._update_technical_configuration()
        return self._ids["product_id"]

    def list_contents(self):
        """List Azure Submissions."""
        if not self._ids["product_id"]:
            self._set_product_id()
        api_response = self._apis["variant"].products_product_id_variants_get(
            product_id=self._ids["product_id"], authorization=self.get_auth()
        )
        return api_response.to_dict()

    def show(self):
        if not self._ids["product_id"]:
            self._set_product_id()

        api_response = self._apis["variant"].products_product_id_variants_get(
            product_id=self._ids["product_id"], authorization=self.get_auth()
        )
        submissions = api_response.to_dict()
        for submission in submissions["value"]:
            if "externalID" in submission and submission["externalID"] == self.plan_name:
                self._ids["plan_id"] = submission["id"]
                return submission
        raise LookupError(f"Plan with this name not found: {self.plan_name}")

    def delete(self) -> {}:
        if not self._ids["plan_id"]:
            self.show()

        self._apis["variant"].products_product_id_variants_variant_id_delete(
            product_id=self._ids["product_id"],
            variant_id=self._ids["plan_id"],
            authorization=self.get_auth(),
        )
        return {}

    def _set_product_id(self):
        """Set Azure Partner Center Product ID"""
        filter_name = "ExternalIDs/Any(i:i/Type eq 'AzureOfferId' and i/Value eq '" + self.name + "')"
        api_response = self._apis["product"].products_get(authorization=self.get_auth(), filter=filter_name)
        submissions = api_response.to_dict()
        for submission in submissions["value"]:
            if submission["name"] == self.name:
                self._ids["product_id"] = submission["id"]
                return submission
        raise LookupError(f"{self.resource_type} with this name not found: {self.name}")

    def _load_plan_config(self, plan_name=None):
        return super()._load_plan_config(plan_name=self.plan_name)

    def _update_plan_listing(self):
        plan_config = self._load_plan_config()
        offer_listing_properties = plan_config["plan_listing"]
        offer_listing_properties["resourceType"] = "AzureListing"
        offer_listing = OfferListing(
            product_id=self.get_product_id(), plan_id=self._ids["plan_id"], authorization=self.get_auth()
        )
        offer_listing.set(properties=offer_listing_properties)

    def _update_pricing_and_availability(self):
        plan_config = self._load_plan_config()
        azure_subscription = plan_config["pricing_and_availability"].get("azure_private_subscriptions", [])
        visibility = plan_config["pricing_and_availability"]["visibility"]
        feature_availability = FeatureAvailability(
            product_id=self.get_product_id(),
            plan_id=self._ids["plan_id"],
            authorization=self.get_auth(),
            subtype=self.subtype,
        )
        try:
            feature_availability.set(azure_subscription=azure_subscription, visibility=visibility)
        except ApiException as error:
            error_message = bytes.decode(error.body).replace("\\", "").split(". ")
            if isinstance(error_message, str):
                raise PermissionError(error_message) from error
            error_json = json.loads(error_message[1].removesuffix('"'))
            raise PermissionError(
                error_message[0].removeprefix('"')
                + "\n"
                + highlight(json.dumps(error_json, indent=4), JsonLexer(), TerminalFormatter())
            ) from error

    def _update_technical_configuration(self):
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        plan_config = self._load_plan_config()

        with open("manifest.yml", encoding="utf8") as file:
            manifest = yaml.safe_load(file)
            file_name = manifest["app"]

        version = plan_config["technical_configuration"]["version"]

        try:
            if self.subtype == "ma":
                allow_jit_access = plan_config["technical_configuration"]["allow_jit_access"]
                policies = plan_config["technical_configuration"]["policy_settings"]

                allowed_customer_actions, allowed_data_actions = self._get_allowed_actions(
                    plan_config["technical_configuration"]
                )
                package = Package(
                    product_id=self.get_product_id(), plan_id=self._ids["plan_id"], authorization=self.get_auth()
                )
                return package.set(
                    app_zip_dir=self.app_path,
                    file_name=file_name,
                    version=version,
                    allow_jit_access=allow_jit_access,
                    resource_type="AzureManagedApplicationPackageConfiguration",
                    policies=policies,
                    allowed_customer_actions=allowed_customer_actions,
                    allowed_data_actions=allowed_data_actions,
                    json_config=json_config,
                )
            if self.subtype == "st":
                package = Package(
                    product_id=self.get_product_id(), plan_id=self._ids["plan_id"], authorization=self.get_auth()
                )
                return package.set(
                    app_zip_dir=self.app_path,
                    file_name=file_name,
                    version=version,
                    resource_type="AzureSolutionTemplatePackageConfiguration",
                )
        except ApiException as error:
            raise ValueError(bytes.decode(error.body).replace("\\", "")) from error

    @staticmethod
    def _get_allowed_actions(json_config):
        allowed_customer_actions = None
        if "allowedCustomerActions" in json_config:
            allowed_customer_actions = json_config["allowedCustomerActions"]
        allowed_data_actions = None
        if "allowedDataActions" in json_config:
            allowed_data_actions = json_config["allowedDataActions"]
        return allowed_customer_actions, allowed_data_actions


class PlanCLIParser(CLIParser):
    """CLI Parser for Marketplace Plans"""

    def __init__(self):
        super().__init__(submission_type=Plan)
        self.parser.add_argument("plan_command", type=str, help="Which plan command to run")
        self.parser.add_argument("--name", type=str, help="Which command to run")

        self._name = "--plan-name"
        self._config_json = "--config-json"

    def _create(self, args):
        return

    def create(self) -> dict:
        """Create a new Application"""
        self.parser.add_argument(
            "--update",
            help="Update App if it exists.",
            type=lambda x: bool(strtobool(x)),
            nargs="?",
            const=True,
            default=False,
        )
        args = self._add_name_config_json_argument()
        try:
            return self.submission_type(
                args.plan_name,
                args.name,
                config_yaml=args.config_yml,
                json_listing_config=args.config_json,
                app_path=args.app_path,
                subtype=args.subgroup,
            ).create()
        except ApiException as error:
            if args.update:
                return self._update(args)
            raise NameError("Plan already exists, try using update instead?") from error

    def list_command(self) -> {}:
        """Create a new Managed Application"""
        args = self.parser.parse_args()
        return self.submission_type(name=args.name, config_yaml=args.config_yml).list_contents()

    def show(self) -> {}:
        """Create a new Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.plan_name, args.name, config_yaml=args.config_yml).show()

    def delete(self) -> {}:
        """Create a new Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.plan_name, args.name, config_yaml=args.config_yml).delete()

    def update(self) -> {}:
        """Create a new Managed Application"""
        args = self._add_name_config_json_argument()
        return self._update(args)

    def _update(self, args):
        return self.submission_type(
            args.plan_name,
            args.name,
            config_yaml=args.config_yml,
            json_listing_config=args.config_json,
            app_path=args.app_path,
            subtype=args.subgroup,
        ).update()

    def publish(self) -> dict:
        """Publish a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.plan_name, args.name, config_yaml=args.config_yml).publish()
