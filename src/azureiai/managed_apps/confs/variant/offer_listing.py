#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Configuration for Offer Listing in Plan Settings"""
from azureiai.managed_apps.confs.offer_configurations import ListingOfferConfigurations
from azureiai.managed_apps.confs.variant.variant_plan_configuration import (
    VariantPlanConfiguration,
)


class OfferListing(ListingOfferConfigurations, VariantPlanConfiguration):
    """Managed Application Variant Offer - Offer Listing Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)
        self.module = "Listing"
        self.get_instance = self.api.products_product_id_listings_get_by_instance_id_instance_i_dinstance_id_get

    def _get_properties(self, properties):
        settings = self.get()
        odata_etag = settings.odata_etag
        settings_id = settings.id
        properties["@odata.etag"] = odata_etag
        properties["id"] = settings_id
        return odata_etag, properties, settings_id
