#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Solution Templates"""
import json
import os

import requests
import yaml
from adal import AuthenticationContext

from azureiai.managed_apps.utils import AAD_CRED, AAD_ID, TENANT_ID
from azureiai.partner_center.cli_parser import CLIParser
from azureiai.partner_center.submission import Submission

AZURE_CONTAINER = "AzureContainer"


class Container(Submission):
    """Azure Partner Center Container Submission"""

    def __init__(
        self,
        name=None,
        config_yaml=r"config.yml",
        app_path: str = ".",
        json_listing_config="ma_config.json",
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_CONTAINER,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )

    def create(self):
        """
        Create Container offer
        First,  verify that the offer does not already exist by checking the offer name.
        If the offer is found, this command should fail, and the user should instead try "update".
        The 'Update' command is used to create a new offer when the offer does not exist.
        """
        try:
            if self.show()["id"]:
                raise NameError("Container offer already exists. Try using 'update'?")
        except ConnectionError:
            pass  # Passing this error is the only way to determine that an offer does not exist
        return self.update()

    def update(self):
        """Update Existing Container offer"""
        headers, json_config, url = self._prepare_request()

        response = requests.put(url, json=json_config, headers=headers)
        if response.status_code != 200:
            raise ConnectionError(json.dumps(response.text, indent=4))
        return response.json()

    def show(self) -> dict:
        """Show the specified existing Container offer"""
        headers, _, url = self._prepare_request()

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ConnectionError(json.dumps(response.text, indent=4))
        return response.json()

    def list_contents(self) -> dict:
        """list only the Container offers"""
        with open(self.config_yaml, encoding="utf8") as file:
            settings = yaml.safe_load(file)

        publisher_id = os.getenv(PUBLISHER_ID, settings["publisherId"])

        offer_type_filter = "offerTypeId eq 'microsoft-azure-container'"
        url = f"{URL_BASE}/{publisher_id}/offers?api-version=2017-10-31&$filter={offer_type_filter}"
        headers = {"Authorization": "Bearer " + self.get_auth(), "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()

    def publish(self):
        """Publish Existing Virtual Machine offer"""
        with open(self.config_yaml, encoding="utf8") as file:
            settings = yaml.safe_load(file)

        offer_id = os.getenv(OFFER_ID, settings["offerId"])
        publisher_id = os.getenv(PUBLISHER_ID, settings["publisherId"])

        url = f"{URL_BASE}/{publisher_id}/offers/{offer_id}/publish?api-version=2017-10-31"

        headers = {"Authorization": "Bearer " + self.get_auth(), "Content-Type": "application/json"}

        response = requests.post(
            url, json={"metadata": {"notification-emails": self.notification_emails}}, headers=headers
        )
        if response.status_code != 202:
            raise ConnectionError(json.dumps(response.text, indent=4))
        return response

    def get_auth(self) -> str:
        """
        Create Authentication Header
        :return: Authorization Header contents
        """
        if self._authorization is None:
            with open(self.config_yaml, encoding="utf8") as file:
                settings = yaml.safe_load(file)

            client_id = os.getenv(AAD_ID, settings["aad_id"])
            client_secret = os.getenv(AAD_CRED, settings["aad_secret"])
            tenant_id = os.getenv(TENANT_ID, settings["tenant_id"])

            auth_context = AuthenticationContext(f"https://login.microsoftonline.com/{tenant_id}")
            token_response = auth_context.acquire_token_with_client_credentials(
                resource="https://cloudpartner.azure.com",
                client_id=client_id,
                client_secret=client_secret,
            )
            self._authorization = token_response["accessToken"]
        return self._authorization

    def _prepare_request(self):
        with open(self.config_yaml, encoding="utf8") as file:
            settings = yaml.safe_load(file)

        offer_id = os.getenv(OFFER_ID, settings["offerId"])
        publisher_id = os.getenv(PUBLISHER_ID, settings["publisherId"])

        url = f"{URL_BASE}/{publisher_id}/offers/{offer_id}?api-version=2017-10-31"
        headers = {"Authorization": "Bearer " + self.get_auth(), "Content-Type": "application/json"}
        return headers, json_config, url


class ContainerCLI(CLIParser):
    """Methods for Container"""

    def __init__(self):
        super().__init__(submission_type=Container)
