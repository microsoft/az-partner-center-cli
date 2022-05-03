#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Virtual Machines"""
import json
import os
from pathlib import Path

import requests
import yaml
from adal import AuthenticationContext

from azureiai.managed_apps.utils import AAD_ID, AAD_CRED, TENANT_ID

from azureiai.partner_center.cli_parser import CLIParser
from azureiai.partner_center.submission import Submission

AZURE_VIRTUAL_MACHINE = "AzureThirdPartyVirtualMachine"
URL_BASE = "https://cloudpartner.azure.com/api/publishers"


class VirtualMachine(Submission):
    """Azure Partner Center Virtual Machine offer."""

    def __init__(
        self,
        name=None,
        notification_emails=None,
        config_yaml=r"config.yml",
        app_path: str = "sample_app",
        json_listing_config="vm_config.json",
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_VIRTUAL_MACHINE,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )
        self.notification_emails = notification_emails

    def update(self):
        """Update Existing Application"""
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        publisher_id = json_config["publisherId"]
        offer_id = json_config["id"]

        url = f"{URL_BASE}/{publisher_id}/offers/{offer_id}?api-version=2017-10-31"
        headers = {"Authorization": "Bearer " + self.get_auth(), "Content-Type": "application/json"}

        response = requests.put(url, json=json_config, headers=headers)
        if response.status_code != 200:
            raise ConnectionError(str(response))

        return response

    def status(self):
        """Get the Status of an Existing Application"""
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        publisher_id = json_config["publisherId"]
        offer_id = json_config["id"]

        url = f"{URL_BASE}/{publisher_id}/offers/{offer_id}/status?api-version=2017-10-31"
        headers = {"Authorization": "Bearer " + self.get_auth(), "Content-Type": "application/json"}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ConnectionError(str(response))

        return response.json()

    def publish(self):
        """Publsih Existing Application"""
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        publisher_id = json_config["publisherId"]
        offer_id = json_config["id"]

        url = f"{URL_BASE}/{publisher_id}/offers/{offer_id}/publish?api-version=2017-10-31"
        headers = {"Authorization": "Bearer " + self.get_auth(), "Content-Type": "application/json"}

        response = requests.post(
            url, json={"metadata": {"notification-emails": self.notification_emails}}, headers=headers
        )
        if response.status_code != 202:
            raise ConnectionError(str(response))

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


class VirtualMachineCLI(CLIParser):
    """Methods for Virtual Machine"""

    def __init__(self):
        super().__init__(submission_type=VirtualMachine)
