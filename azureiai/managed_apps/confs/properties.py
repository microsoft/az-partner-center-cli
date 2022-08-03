#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Properties settings for Plan configuration"""
import uuid

from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from swagger_client import PropertyApi


class Properties(OfferConfigurations):
    """Managed Application Offer - Properties Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)
        self.api = PropertyApi()
        self.module = "Property"
        self.get_instance = self.api.products_product_id_properties_get_by_instance_id_instance_i_dinstance_id_get

    def set(
        self,
        version,
        use_enterprise_contract=True,
        leveled_categories=None,
    ):
        """
        Set Properties for Application

        :param version: E.g. 1.1.1
        :param use_enterprise_contract: Default: True
        :param leveled_categories: Default: {}
        """
        leveled_categories = leveled_categories or {}

        property_settings = self.get()
        odata_etag = property_settings.odata_etag
        property_id = property_settings.id

        submission_version = str(uuid.uuid4())

        properties = {
            "resourceType": "AzureProperty",
            "industries": [""],
            "submissionVersion": submission_version,
            "productTags": ["y89royn4xnxbe5e9mfmm6ukufp1hn8gt6d6osyd83sprfgdtib8jqfmikiya5hmf"],
            "appVersion": version,
            "useEnterpriseContract": use_enterprise_contract,
            "termsOfUse": "testTermsOfUse",
            "globalAmendmentTerms": None,
            "customAmendments": [],
            "leveledCategories": leveled_categories,
            "@odata.etag": odata_etag,
        }

        self.api.products_product_id_properties_property_id_put(
            authorization=self.authorization,
            if_match=odata_etag,
            product_id=self.product_id,
            property_id=property_id,
            body=properties,
        )
