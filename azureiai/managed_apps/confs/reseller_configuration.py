#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Reseller Settings for Plan configurations"""
from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from swagger_client import ResellerConfigurationApi


class ResellerConfiguration(OfferConfigurations):
    """Managed Application Offer - Reseller Configuration Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)
        self.api = ResellerConfigurationApi()

    def get(self):
        """Get Availability for Application"""
        return self.api.products_product_id_reseller_configuration_get(
            product_id=self.product_id, authorization=self.authorization
        )

    def set(self, reseller_channel_state="Disabled"):
        """
        Set Availability for Application

        :param reseller_channel_state: must be one of ['PartialOptIn', 'Disabled', 'Optin']
        """
        if reseller_channel_state not in ["PartialOptIn", "Disabled", "Optin"]:
            raise ValueError(
                "Not a known value, expected one of the following: 'PartialOptIn', 'Disabled', 'Optin'; but got ",
                reseller_channel_state,
            )
        properties = {
            "resourceType": "ResellerConfiguration",
            "ResellerChannelState": reseller_channel_state,
            "TenantIds": [],
        }

        self.api.products_product_id_reseller_configuration_post(
            authorization=self.authorization,
            product_id=self.product_id,
            body=properties,
        )
