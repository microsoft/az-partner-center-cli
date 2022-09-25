#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Offer Interface"""
from abc import abstractmethod

from azureiai.managed_apps.confs import ResellerConfiguration
from azureiai.managed_apps.confs.variant import FeatureAvailability
from azureiai.managed_apps.utils import (
    get_draft_instance_id,
    get_variant_draft_instance_id,
)
from swagger_client import (
    BranchesApi,
    ProductApi,
    ProductAvailabilityApi,
    PropertyApi,
    SubmissionApi,
    VariantApi,
)


class AbstractOffer:
    """Azure Partner Portal - Offer Interface"""

    def __init__(self, name=None):
        self.name = name
        self._authorization = None

        self._apis = {
            "product": ProductApi(),
            "variant": VariantApi(),
            "property": PropertyApi(),
            "branches": BranchesApi(),
            "product_availability": ProductAvailabilityApi(),
            "submission": SubmissionApi(),
        }

        self._ids = {
            "product_id": "",
            "plan_id": None,
            "submission_id": None,
            "availability_draft_instance_id": None,
            "availability_id": None,
            "offer_id": "",
        }

    @abstractmethod
    def get_auth(self) -> str:
        """
        Create Authentication Header

        :return: Authorization Header contents
        """

    def get_product_id(self) -> str:
        """
        Get or Set Product ID

        Will call create method if AMA has not yet been created.
        :return: Product ID of new Managed Application
        """

        if self._ids["product_id"] == "":
            self.create()
        return self._ids["product_id"]

    def get_offer_id(self) -> str:
        """
        Get Offer ID

        Return Offer ID generated at creation time.
        :return: Offer ID of new Managed Application
        """
        if self._ids["offer_id"] == "":
            self.create()
        return self._ids["offer_id"]

    def get_plan_id(self) -> str:
        """
        Get or Set Product ID

        Will call create method if AMA has not yet been created.
        :return: Product ID of new Managed Application
        """

        if self._ids["plan_id"] == "":
            self.create()
        return self._ids["plan_id"]

    @abstractmethod
    def create(self) -> str:
        """Create new Azure Managed Application and set product id."""

    def _get_draft_instance_id(self, module: str, retry: int = 0):
        """Call Branch API to get Configuration ID"""
        return get_draft_instance_id(self.get_product_id(), self.get_auth(), module, retry)

    def _get_variant_draft_instance_id(self, module: str, retry: int = 0) -> str:
        return get_variant_draft_instance_id(self.get_product_id(), self.get_auth(), module, retry)

    def _set_resell_through_csps(self):
        reseller = ResellerConfiguration(product_id=self.get_product_id(), authorization=self.get_auth())
        reseller.set()

    def _set_pricing_and_availability(self, azure_subscription):
        feature_availability = FeatureAvailability(
            product_id=self.get_product_id(), plan_id=self.get_plan_id(), authorization=self.get_auth()
        )
        feature_availability.set(azure_subscription=azure_subscription)
