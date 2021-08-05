#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""The feature availability configuration sets the visibility of the Azure Marketplace offer"""
import json
from pathlib import Path

from swagger_client import FeatureAvailabilityApi

from azureiai.managed_apps.confs.variant.variant_plan_configuration import (
    VariantPlanConfiguration,
)


class FeatureAvailability(VariantPlanConfiguration):
    """Managed Application Offer - Feature Availability Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)
        self.fa_api = FeatureAvailabilityApi()

    def get(self):
        """Get Availability for Application"""
        instance_id = self._get_draft_instance_id(module="Availability")
        resp = self.fa_api.products_product_id_feature_availabilities_get_by_instance_id_instance_i_dinstance_id_get(
            product_id=self.product_id,
            instance_id=instance_id,
            authorization=self.authorization,
            expand="MarketStates,Trial,PriceSchedules",
        )
        self.setting_id = resp.value[0].id
        return resp.value[0]

    def set(
        self,
        azure_subscription,
        visibility="Private",
    ):
        """Set Availability for Application

        :param azure_subscription: Azure Subscriptions with access to application
        :param visibility: Public or Private
        """
        settings = self.get()
        odata_etag = settings.odata_etag
        settings_id = settings.id

        market_states = self.get_markets()
        market_states[130]["state"] = "Enabled"

        body = {
            "resourceType": "FeatureAvailability",
            "visibility": visibility,
            "marketStates": market_states,
            "subscriptionAudiences": [{"ID": azure_subscription}],
            "priceSchedules": [
                {
                    "isBaseSchedule": False,
                    "marketCodes": ["US"],
                    "friendlyName": "free_priceOverrideSchedule_US",
                    "schedules": [
                        {
                            "retailPrice": {"openPrice": 0, "currencyCode": "USD"},
                            "priceCadence": {"type": "Month", "value": 1},
                            "pricingModel": "Recurring",
                        }
                    ],
                }
            ],
            "@odata.etag": odata_etag,
            "id": settings_id,
        }
        self.fa_api.products_product_id_featureavailabilities_feature_availability_id_put(
            authorization=self.authorization,
            if_match=odata_etag,
            product_id=self.product_id,
            feature_availability_id=settings_id,
            body=body,
            expand="MarketStates,Trial,PriceSchedules",
        )

    @staticmethod
    def get_markets():
        """
        Get list of all markets used for published to application.

        :return: Dict of markets loaded from json
        """
        market_json = Path(__file__).parents[0].joinpath("markets.json")
        with open(market_json, "r") as json_file:
            data = json_file.read()
            return json.loads(data)
