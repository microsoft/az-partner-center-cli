#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Properties settings for Plan configuration"""
import uuid

from swagger_client import PropertyApi

from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations


class Properties(OfferConfigurations):
    """Managed Application Offer - Properties Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)
        self.api = PropertyApi()
        self.module = "Property"
        self.get_instance = self.api.products_product_id_properties_get_by_instance_id_instance_i_dinstance_id_get

    def set(
        self,
        industries,
        categories,
        version,
        use_enterprise_contract=True,
    ):
        """
        Set Properties for Application

        :param industries: Default: Retail
        :param categories:  Default: analytics
        :param version: Default 1.1.1
        :param use_enterprise_contract: Default: True
        """
        property_settings = self.get()
        odata_etag = property_settings.odata_etag
        property_id = property_settings.id

        submission_version = str(uuid.uuid4())

        properties = {
            "resourceType": "AzureProperty",
            "industries": [industries],
            "categories": [categories],
            "submissionVersion": submission_version,
            "productTags": ["y89royn4xnxbe5e9mfmm6ukufp1hn8gt6d6osyd83sprfgdtib8jqfmikiya5hmf"],
            "appVersion": version,
            "useEnterpriseContract": use_enterprise_contract,
            "termsOfUse": "testTermsOfUse",
            "globalAmendmentTerms": None,
            "customAmendments": [],
            "leveledCategories": {},
            "@odata.etag": odata_etag,
        }

        self.api.products_product_id_properties_property_id_put(
            authorization=self.authorization,
            if_match=odata_etag,
            product_id=self.product_id,
            property_id=property_id,
            body=properties,
        )

    @classmethod
    def create(cls, ama, json_config):
        industries = json_config["industries"]
        categories = json_config["categories"]
        version = json_config["version"]

        offer_listing_properties = cls(product_id=ama.get_product_id(), authorization=ama.get_auth())
        offer_listing_properties.set(industries=industries, categories=categories, version=version)
        return offer_listing_properties
