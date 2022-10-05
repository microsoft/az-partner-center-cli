#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""The feature availability configuration sets the visibility of the Azure Marketplace offer"""
import json
from pathlib import Path

from azureiai.managed_apps.confs.variant.variant_plan_configuration import (
    VariantPlanConfiguration,
)
from swagger_client import FeatureAvailabilityApi


class FeatureAvailability(VariantPlanConfiguration):
    """Managed Application Offer - Feature Availability Configuration"""

    def _get_properties(self, properties):
        pass

    def __init__(self, product_id, plan_id, authorization, subtype="ma"):
        super().__init__(product_id, plan_id, authorization, subtype)
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

        if self.subtype == "ma":
            market_states = self.get_markets()
            market_states[130]["state"] = "Enabled"

            body = {
                "resourceType": "FeatureAvailability",
                "visibility": visibility,
                "marketStates": market_states,
                "@odata.etag": odata_etag,
                "id": settings_id,
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
            }
        else:
            body = {
                "resourceType": "FeatureAvailability",
                "visibility": visibility,
                "@odata.etag": odata_etag,
                "id": settings_id,
            }

        if visibility == "Private":
            body["subscriptionAudiences"] = azure_subscription

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
        with open(market_json, "r", encoding="utf8") as json_file:
            data = json_file.read()
            return json.loads(data)
