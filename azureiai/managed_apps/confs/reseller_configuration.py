#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Reseller Settings for Plan configurations"""
import os

from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from swagger_client import ResellerConfigurationApi, ResellerConfiguration as Body

DEFAULT_STATE = "Enabled"


class ResellerConfiguration(OfferConfigurations):
    """Managed Application Offer - Reseller Configuration Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)
        self.api = ResellerConfigurationApi()

    def get(self):
        """Get Availability for Application"""
        return self.api.list(product_id=self.product_id, authorization=self.authorization)

    def set(self, reseller_channel_state=DEFAULT_STATE):
        """
        Set Availability for Application

        :param reseller_channel_state: must be one of ['PartialOptIn', 'Disabled', 'OptIn']
        """
        reseller_channel_state = os.getenv("RESELLER_CHANNEL", reseller_channel_state)
        if reseller_channel_state not in ["PartialOptIn", "Disabled", "Enabled"]:
            raise ValueError(
                "Not a known value, expected one of the following: 'PartialOptIn', 'Disabled', 'Enabled'; but got ",
                reseller_channel_state,
            )
        body = Body(resource_type="ResellerConfiguration", reseller_channel_state=reseller_channel_state, tenant_ids=[])
        self.api.create(
            authorization=self.authorization,
            product_id=self.product_id,
            body=body,
        )
