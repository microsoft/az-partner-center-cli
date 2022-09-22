#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Product Availability settings for Offer Configuration"""
from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from swagger_client import PreviewMarketplaceGroup, ProductAvailabilityApi, ProductAvailability as Body


class ProductAvailability(OfferConfigurations):
    """Managed Application Offer - Product Availability Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)

        self.api = ProductAvailabilityApi()
        self.module = "Availability"
        self.get_instance = self.api.get_by

        self._settings = None
        self.setting_id = None

    def set(
        self,
        azure_subscription,
        visibility="Public",
    ):
        """Set Availability for Application

        :param azure_subscription: Azure Subscriptions with access to Azure Managed Application
        :param visibility: Public or Private
        """
        settings = self.get()
        odata_etag = settings.odata_etag
        settings_id = settings.id
        audiences = PreviewMarketplaceGroup(values=azure_subscription)
        body = Body(
            visibility=visibility,
            audiences=[audiences],
            odata_etag=odata_etag,
            id=settings_id,
        )
        self.api.set(
            authorization=self.authorization,
            if_match=odata_etag,
            product_id=self.product_id,
            product_availability_id=settings_id,
            body=body,
        )
