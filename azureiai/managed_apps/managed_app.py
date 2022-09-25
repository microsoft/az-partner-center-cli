#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""This module contains methods and classes for Azure Managed Application publication."""
from __future__ import absolute_import

import json
import os
import uuid
from pathlib import Path

import yaml

from azureiai import RetryException
from azureiai.managed_apps.confs import (
    Listing,
    ListingImage,
    ProductAvailability,
    Properties,
)
from azureiai.managed_apps.confs.variant import (
    FeatureAvailability,
    OfferListing,
    Package,
)
from azureiai.managed_apps.counter import inc_counter
from azureiai.partner_center.offer import Offer
from swagger_client.rest import ApiException


class ManagedApplication(Offer):
    """
    Azure Managed Application

    Used to get, create, or delete an AMA based on product_id.
    """

    def set_product_id(self, product_id: str):
        """
        Set Product ID from existing application.

        :param product_id: Product ID of existing managed application.
        """
        self._ids["product_id"] = product_id

    def set_offer_id(self, offer_id: str):
        """
        Set Offer ID from existing application.

        :param offer_id: Offer ID of existing managed application.
        """
        self._ids["plan_id"] = offer_id

    def create(self):
        """Create new Azure Managed Application and set product id."""
        offer_id = str(uuid.uuid4())
        self._ids["offer_id"] = offer_id

        body = {
            "resourceType": "AzureApplication",
            "name": self.name,
            "externalIDs": [{"type": "AzureOfferId", "value": offer_id}],
            "isModularPublishing": True,
        }
        api_response = self._apis["product"].products_post(authorization=self.get_auth(), body=body)
        self._ids["product_id"] = api_response.id

    def delete(self):
        """
        Delete instance of Azure Managed Application.

        :return: product delete api response
        """
        return self._apis["product"].products_product_id_delete(
            product_id=self.get_product_id(), authorization=self.get_auth()
        )

    def manifest_publish(self, manifest_yml, config_yml) -> bool:
        """
        Prepare to Publish Application using Manifest File.

        :param manifest_yml: path to manifest.yml, see template.manifest.yml for example.
        :param config_yml: path to config.yml, see template.config.yml for example.
        :return: Publish Outcome
        """
        with open(manifest_yml, encoding="utf8") as file:
            manifest = yaml.safe_load(file)
        return self.prepare_publish(
            plan_name=manifest["plan_name"],
            app_path=manifest["app_path"],
            app=manifest["app"],
            json_listing_config=manifest["json_listing_config"],
            config_yml=config_yml,
        )

    def prepare_plan(
        self,
        plan_name: str,
        app_path: str,
        app: str,
        json_listing_config: str = "json_config.json",
        config_yml: str = "config.yml",
    ) -> bool:
        """
        Create new AMA and complete all fields for publication.

        :param plan_name: Display Name of Plan
        :param app_path: Path to Managed Application Zip. Example: C:\\User\\
        :param app: Managed Application Zip (including extension). Example: my_app.zip
        :param json_listing_config:
        :param config_yml: Configuration YML, see README for directions to config

        :return: binary outcome of preparation
        """

        if not os.path.isfile(os.path.join(app_path, app)):
            raise FileNotFoundError("Managed Application Zip - Not Found", os.path.join(app_path, app))
        if not os.path.isfile(os.path.join(app_path, json_listing_config)):
            raise FileNotFoundError("JSON Config - Not Found")
        with open(Path(app_path).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        self._create_plan(app, app_path, config_yml, json_config, plan_name)

        return True

    def prepare_publish(
        self,
        plan_name: str,
        app_path: str,
        app: str,
        json_listing_config: str = "json_config.json",
        config_yml: str = "config.yml",
    ) -> bool:
        """
        Create new AMA and complete all fields for publication.

        :param plan_name: Display Name of Plan
        :param logo_large: PNG 216x216 Pixels
        :param logo_small: PNG 48x48 Pixels
        :param logo_medium: PNG 90x90 Pixels
        :param logo_wide: PNG 255x115 Pixels
        :param app_path: Path to Managed Application Zip. Example: C:\\User\\
        :param app: Managed Application Zip (including extension). Example: my_app.zip
        :param json_listing_config:
        :param config_yml: Configuration YML, see README for directions to config

        :return: binary outcome of preparation
        """

        if not os.path.isfile(os.path.join(app_path, app)):
            raise FileNotFoundError(f"Managed Application Zip - Not Found - {app_path}{os.path.sep}{app}")
        if not os.path.isfile(os.path.join(app_path, json_listing_config)):
            raise FileNotFoundError("JSON Config - Not Found")
        with open(Path(app_path).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        self._create_plan(app, app_path, config_yml, json_config, plan_name)

        self._set_properties(json_config)
        self._set_offer_listing(app_path, json_listing_config, update_image=True)
        self._set_plan_listing(json_config)

        self._set_preview_audience(json_config)

        self._set_resell_through_csps()

        return True

    def publish(self):
        """
        Create new AMA and complete all fields for publication

        :return: submission post api response
        """

        body = {
            "resourceType": "SubmissionCreationRequest",
            "targets": [{"type": "Scope", "value": "preview"}],
            "resources": [
                {"type": "Availability", "value": self._get_draft_instance_id("Availability")},
                {"type": "Property", "value": self._get_draft_instance_id("Property")},
                {"type": "Package", "value": self._get_draft_instance_id("Package")},
                {"type": "Listing", "value": self._get_draft_instance_id("Listing")},
                {"type": "Cosell", "value": self._get_draft_instance_id("Cosell")},
                {"type": "ResellerConfiguration", "value": self.get_product_id() + "-ResellerInstance"},
            ],
            "variantResources": [
                {
                    "variantID": self._ids["plan_id"],
                    "resources": [
                        {"type": "Availability", "value": self._get_variant_draft_instance_id("Availability")},
                        {"type": "Package", "value": self._get_variant_draft_instance_id("Package")},
                        {"type": "Listing", "value": self._get_variant_draft_instance_id("Listing")},
                    ],
                }
            ],
        }

        response = self._apis["submission"].products_product_id_submissions_post(
            authorization=self.get_auth(),
            product_id=self.get_product_id(),
            body=body,
        )

        self._ids["submission_id"] = response.id
        return response

    def submission_status(self):
        """
        Get Submission Status

        :return: submission api response
        """
        return self._apis["submission"].products_product_id_submissions_get(
            authorization=self.get_auth(),
            product_id=self.get_product_id(),
        )

    def update(
        self, app_path: str, app: str, json_listing_config, config_yml: str = "config.yml", update_image: bool = True
    ):
        """
        Update existing AMA and complete all fields for publication.

        :param app_path: Path to Managed Application Zip. Example: C:\\User\\
        :param app: Managed Application Zip (including extension). Example: my_app.zip
        :param json_listing_config:
        :param config_yml: Configuration YML, see README for directions to config
        :param update_image: Select if photos should be updated, default: True

        :return: binary outcome of preparation
        """
        with open(Path(app_path).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        self._set_properties(json_config)
        self._set_offer_listing(app_path, json_listing_config, update_image)
        self._set_plan_listing(json_config)
        self._set_preview_audience(json_config)

        return self._set_technical_configuration(
            json_config,
            app,
            app_path,
            config_yml,
        )

    def _create_new_plan(self, plan_name: str, retry=0):
        """
        Create new AMA Plan and retry up to 5 times.

        :param plan_name: Display Name of Plan
        :param retry: number of times to retry
        return: variant post api response
        """
        body = {
            "resourceType": "AzureSkuVariant",
            "state": "Active",
            "friendlyName": plan_name,
            "leadGenID": "publisher_name." + self.name + plan_name,
            "externalID": self.name + plan_name,
            "cloudAvailabilities": ["public-azure"],
            "SubType": "managed-application",
        }

        try:
            api_response = self._apis["variant"].products_product_id_variants_post(
                authorization=self.get_auth(),
                product_id=self.get_product_id(),
                body=body,
            )
            self._ids["plan_id"] = api_response["id"]
            return api_response
        except ApiException as api_expection:
            if retry < 5:
                return self._create_new_plan(plan_name=plan_name, retry=retry + 1)
            raise RetryException() from api_expection

    @staticmethod
    def _load_plan_config(json_config):
        plan_overview = json_config["plan_overview"]
        if isinstance(plan_overview, list):
            return plan_overview[0]
        return plan_overview[next(iter(plan_overview))]

    def _set_plan_listing(self, json_config):
        plan_config = self._load_plan_config(json_config)
        offer_listing_properties = plan_config["plan_listing"]
        offer_listing = OfferListing(
            product_id=self.get_product_id(), plan_id=self.get_plan_id(), authorization=self.get_auth()
        )
        offer_listing.set(properties=offer_listing_properties)

    def _set_offer_listing(self, app_path, json_listing_config, update_image=False):
        with open(Path(app_path).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        listing = Listing(product_id=self.get_product_id(), authorization=self.get_auth())
        listing.set(properties=Path(app_path).joinpath(json_listing_config))

        if update_image:
            logo_large = json_config["offer_listing"]["listing_logos"]["logo_large"]
            logo_medium = json_config["offer_listing"]["listing_logos"]["logo_medium"]
            logo_small = json_config["offer_listing"]["listing_logos"]["logo_small"]
            logo_wide = json_config["offer_listing"]["listing_logos"]["logo_wide"]

            if not os.path.isfile(os.path.join(app_path, logo_large)):
                raise FileNotFoundError("Logo Large - Not Found")
            if not os.path.isfile(os.path.join(app_path, logo_small)):
                raise FileNotFoundError("Logo Small - Not Found")
            if not os.path.isfile(os.path.join(app_path, logo_medium)):
                raise FileNotFoundError("Logo Medium - Not Found")
            if not os.path.isfile(os.path.join(app_path, logo_wide)):
                raise FileNotFoundError("Logo Wide - Not Found")

            listing_image = ListingImage(product_id=self.get_product_id(), authorization=self.get_auth())
            listing_image.set(file_name=logo_large, file_path=app_path, logo_type="AzureLogoLarge")
            listing_image.set(file_name=logo_small, file_path=app_path, logo_type="AzureLogoSmall")
            listing_image.set(file_name=logo_medium, file_path=app_path, logo_type="AzureLogoMedium")
            listing_image.set(file_name=logo_wide, file_path=app_path, logo_type="AzureLogoWide")

    def _set_properties(self, json_config):
        plan_config = self._load_plan_config(json_config)
        version = plan_config["technical_configuration"]["version"]

        offer_listing_properties = Properties(product_id=self.get_product_id(), authorization=self.get_auth())
        offer_listing_properties.set(version=version)

    def _set_preview_audience(self, json_config):
        azure_subscription = json_config["preview_audience"]["subscriptions"]

        availability = ProductAvailability(product_id=self.get_product_id(), authorization=self.get_auth())
        availability.set(azure_subscription=azure_subscription)

    def _create_plan(self, app, app_path, config_yml, json_config, plan_name):

        plan_config = self._load_plan_config(json_config)
        azure_subscription = plan_config["pricing_and_availability"]["azure_private_subscriptions"]
        self._create_new_plan(plan_name=plan_name)

        self._set_technical_configuration(
            json_config,
            app,
            app_path,
            config_yml,
        )

        self._set_pricing_and_availability(azure_subscription)

    def _set_pricing_and_availability(self, azure_subscription):
        feature_availability = FeatureAvailability(
            product_id=self.get_product_id(), plan_id=self.get_plan_id(), authorization=self.get_auth()
        )
        feature_availability.set(azure_subscription=azure_subscription)

    def _set_technical_configuration(
        self,
        json_config,
        app,
        app_path,
        config_yml,
    ):

        plan_config = self._load_plan_config(json_config)
        version = plan_config["technical_configuration"]["version"]

        allow_jit_access = plan_config["technical_configuration"]["allow_jit_access"]
        policies = plan_config["technical_configuration"]["policy_settings"]

        allowed_customer_actions, allowed_data_actions = self._get_allowed_actions(json_config)
        package = Package(product_id=self.get_product_id(), plan_id=self.get_plan_id(), authorization=self.get_auth())
        return package.set(
            app_zip_dir=app_path,
            file_name=app,
            version=version,
            allow_jit_access=allow_jit_access,
            policies=policies,
            allowed_customer_actions=allowed_customer_actions,
            allowed_data_actions=allowed_data_actions,
            json_config=json_config,
        )

    @staticmethod
    def _get_allowed_actions(json_config):
        allowed_customer_actions = None
        plan_config = ManagedApplication._load_plan_config(json_config)
        if "allowedCustomerActions" in plan_config:
            allowed_customer_actions = plan_config["technical_configuration"]["allowedCustomerActions"]
        allowed_data_actions = None
        if "allowedDataActions" in plan_config:
            allowed_data_actions = plan_config["technical_configuration"]["allowedDataActions"]
        return allowed_customer_actions, allowed_data_actions

    def _get_variant_draft_instance_id(self, module: str, retry: int = 0) -> str:
        api_response = self._apis["branches"].products_product_id_branches_get_by_module_modulemodule_get(
            product_id=self.get_product_id(),
            module=module,
            authorization=self.get_auth(),
        )
        if not api_response.value:
            if retry < 3:
                return self._get_variant_draft_instance_id(module=module, retry=retry + 1)
            raise RetryException("Retry Failed")
        i = inc_counter(api_response)
        return api_response.value[i].current_draft_instance_id

    def promote(self):
        """
        Promote Application

        :return: submission api response
        """
        return self._apis["submission"].products_product_id_submissions_submission_id_promote_post(
            product_id=self.get_product_id(),
            submission_id=self._ids["submission_id"],
            authorization=self.get_auth(),
        )

    def get_offers(self):
        """
        List Existing Managed Applications

        :return: List of managed applications.
        """
        return self._apis["product"].products_get(authorization=self.get_auth())
