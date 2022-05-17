#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Offer Interface"""
from abc import abstractmethod

import yaml
from adal import AuthenticationContext
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import CredentialUnavailableError

from azureiai.managed_apps.confs import ResellerConfiguration
from azureiai.managed_apps.confs.variant import FeatureAvailability
from azureiai.managed_apps.utils import (
    get_draft_instance_id,
    get_variant_draft_instance_id,
    CONFIG_YML,
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

    def __init__(self, name=None, config_yaml=CONFIG_YML):
        self.name = name
        self.config_yaml = config_yaml
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

    def get_auth(self) -> str:
        """
        Create Authentication Header

        :return: Authorization Header contents
        """
        if self._authorization is None:
            try:
                from azure.identity import AzureCliCredential
                from azure.mgmt.resource import SubscriptionClient

                credential = AzureCliCredential()
                token = credential.get_token("https://api.partner.microsoft.com").token
                self._authorization = f"Bearer {token}"
            except (CredentialUnavailableError, ClientAuthenticationError):

                with open(self.config_yaml, encoding="utf8") as file:
                    settings = yaml.safe_load(file)

                client_id = settings["aad_id"]
                client_secret = settings["aad_secret"]
                tenant_id = settings["tenant_id"]

                auth_context = AuthenticationContext(f"https://login.microsoftonline.com/{tenant_id}")
                token_response = auth_context.acquire_token_with_client_credentials(
                    resource="https://api.partner.microsoft.com",
                    client_id=client_id,
                    client_secret=client_secret,
                )
                self._authorization = f"Bearer {token_response['accessToken'].token}"
        return self._authorization

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
        feature_availability = FeatureAvailability(product_id=self.get_product_id(), authorization=self.get_auth())
        feature_availability.set(azure_subscription=azure_subscription)
