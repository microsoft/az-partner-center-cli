#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Managed Applications"""
import json
import os
from pathlib import Path

from azureiai.managed_apps.confs import Properties, ProductAvailability, Listing, ListingImage, ResellerConfiguration
from azureiai.managed_apps.confs.reseller_configuration import DEFAULT_STATE
from azureiai.partner_center.offer import Offer
from swagger_client.rest import ApiException


class Submission(Offer):
    """New Version of Offer used for v2 CLI"""

    def __init__(
        self,
        name=None,
        config_yaml: str = "config.yml",
        resource_type: str = "",
        app_path: str = ".",
        json_listing_config: str = "listing_config.json",
    ):
        super().__init__(name, config_yaml)
        self.resource_type = resource_type
        self.app_path = app_path
        self.json_listing_config = json_listing_config

    def list_contents(self):
        """List Azure Submissions."""
        api_response = self._apis["product"].products_get(
            authorization=self.get_auth(), filter=f"ResourceType eq '{self.resource_type}'"
        )
        return api_response.to_dict()

    def create(self) -> dict:
        """Create new Azure Submission and set product id."""
        body = {
            "resourceType": self.resource_type,
            "name": self.name,
            "externalIDs": [{"type": "AzureOfferId", "value": self.name}],
            "isModularPublishing": True,
        }
        try:
            api_response = self._apis["product"].products_post(authorization=self.get_auth(), body=body)
        except ApiException as error:
            raise NameError("Application already exists. Try using 'update'?") from error

        self._ids["product_id"] = api_response.id
        self.update()
        return api_response.to_dict()

    def update(self):
        """Update Existing Application"""
        if not self._ids["product_id"]:
            self.show()

        self._update_properties()
        self._update_offer_listing()
        self._update_preview_audience()
        self._set_resell_through_csps()

        return self._ids["product_id"]

    def show(self):
        """Show details of an Azure Submission"""
        filter_name = "ExternalIDs/Any(i:i/Type eq 'AzureOfferId' and i/Value eq '" + self.name + "')"
        api_response = self._apis["product"].products_get(authorization=self.get_auth(), filter=filter_name)
        submissions = api_response.to_dict()
        for submission in submissions["value"]:
            if submission["name"] == self.name:
                self._ids["product_id"] = submission["id"]
                return submission
        raise LookupError(f"{self.resource_type} with this name not found: {self.name}")

    def delete(self):
        """List Azure Submissions."""
        if not self._ids["product_id"]:
            self.show()
        api_response = self._apis["product"].products_product_id_delete(
            product_id=self._ids["product_id"], authorization=self.get_auth()
        )
        return api_response

    def publish(self):
        """Publish Submission by submitting Instance IDs"""
        if not self._ids["product_id"]:
            self.show()
        body = {
            "resourceType": "SubmissionCreationRequest",
            "targets": [{"type": "Scope", "value": "preview"}],
            "resources": [
                {"type": "Availability", "value": self._get_draft_instance_id("Availability")},
                {"type": "Property", "value": self._get_draft_instance_id("Property")},
                {"type": "Package", "value": self._get_draft_instance_id("Package")},
                {"type": "Listing", "value": self._get_draft_instance_id("Listing")},
                {"type": "ResellerConfiguration", "value": self.get_product_id() + "-ResellerInstance"},
            ],
            "variantResources": [],
        }

        response = self._apis["variant"].products_product_id_variants_get(
            product_id=self._ids["product_id"], authorization=self.get_auth()
        )

        for variant in response.to_dict()["value"]:
            if variant["id"] != "testdrive":
                body["variantResources"] += [
                    {
                        "variantID": variant["id"],
                        "resources": [
                            {
                                "type": "Availability",
                                "value": self._get_variant_draft_instance_id(variant["id"], "Availability"),
                            },
                            {"type": "Package", "value": self._get_variant_draft_instance_id(variant["id"], "Package")},
                            {"type": "Listing", "value": self._get_variant_draft_instance_id(variant["id"], "Listing")},
                        ],
                    }
                ]

        try:
            response = self._apis["submission"].products_product_id_submissions_post(
                authorization=self.get_auth(),
                product_id=self.get_product_id(),
                body=body,
            )
        except ApiException as error:
            raise SystemError(
                "Publish Failed! An internal error occurred when trying to publish the package"
            ) from error
        self._ids["submission_id"] = response.id

        return self._apis["submission"].products_product_id_submissions_submission_id_get(
            authorization=self.get_auth(),
            product_id=self.get_product_id(),
            submission_id=response.id,
        )

    def release(self):
        """
        Release Marketplace Application by submitting Submission ID

        :return: Submission API Response
        """
        try:
            return self._apis["submission"].products_product_id_submissions_submission_id_promote_post(
                product_id=self.get_product_id(),
                submission_id=self.get_submission_id(),
                authorization=self.get_auth(),
            )
        except ApiException as error:
            raise SystemError("Release Failed! Is preview creation in progress?") from error

    def _load_plan_config(self, plan_name: str = None):
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        plan_overview = json_config["plan_overview"]
        if isinstance(plan_overview, list):
            return plan_overview[0]
        if plan_name:
            return plan_overview[plan_name]
        return plan_overview[next(iter(plan_overview))]

    def _update_properties(self):
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)
        plan_config = self._load_plan_config()

        leveled_categories = json_config["property_settings"].get("leveledCategories", {})
        version = plan_config["technical_configuration"]["version"]

        offer_listing_properties = Properties(product_id=self.get_product_id(), authorization=self.get_auth())
        offer_listing_properties.set(
            version,
            leveled_categories=leveled_categories,
        )

    def _set_resell_through_csps(self):
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)
            reseller_channel_state = json_config["offer_listing"].get("reseller_channel", DEFAULT_STATE)

        reseller = ResellerConfiguration(product_id=self.get_product_id(), authorization=self.get_auth())
        reseller.set(reseller_channel_state=reseller_channel_state)

    def _update_preview_audience(self):
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        azure_subscription = json_config["preview_audience"]["subscriptions"]
        availability = ProductAvailability(product_id=self.get_product_id(), authorization=self.get_auth())
        availability.set(azure_subscription=azure_subscription)

    def _update_offer_listing(self, update_image=True):
        listing = Listing(product_id=self.get_product_id(), authorization=self.get_auth())
        listing.set(properties=Path(self.app_path).joinpath(self.json_listing_config))

        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        if update_image:
            logo_large = json_config["offer_listing"]["listing_logos"]["logo_large"]
            logo_medium = json_config["offer_listing"]["listing_logos"]["logo_medium"]
            logo_small = json_config["offer_listing"]["listing_logos"]["logo_small"]
            logo_wide = json_config["offer_listing"]["listing_logos"]["logo_wide"]

            if not os.path.isfile(os.path.join(self.app_path, logo_large)):
                raise FileNotFoundError(f"Logo Large not Found at location: {self.app_path}/{logo_large}")
            if not os.path.isfile(os.path.join(self.app_path, logo_small)):
                raise FileNotFoundError(f"Logo Small not Found at location: {self.app_path}/{logo_small}")
            if not os.path.isfile(os.path.join(self.app_path, logo_medium)):
                raise FileNotFoundError(f"Logo Medium not Found at location: {self.app_path}/{logo_medium}")
            if not os.path.isfile(os.path.join(self.app_path, logo_wide)):
                raise FileNotFoundError(f"Logo Wide not Found at location: {self.app_path}/{logo_wide}")

            listing_image = ListingImage(product_id=self.get_product_id(), authorization=self.get_auth())
            listing_image.set(file_name=logo_large, file_path=self.app_path, logo_type="AzureLogoLarge")
            listing_image.set(file_name=logo_small, file_path=self.app_path, logo_type="AzureLogoSmall")
            listing_image.set(file_name=logo_medium, file_path=self.app_path, logo_type="AzureLogoMedium")
            listing_image.set(file_name=logo_wide, file_path=self.app_path, logo_type="AzureLogoWide")
