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

from azureiai.managed_apps.utils import AAD_CRED, AAD_ID, TENANT_ID
from azureiai.partner_center.cli_parser import CLIParser
from azureiai.partner_center.submission import Submission

AZURE_VIRTUAL_MACHINE = "AzureThirdPartyVirtualMachine"
RESOURCE_CPP_API = "https://cloudpartner.azure.com"
RESOURCE_PC_API = "https://api.partner.microsoft.com"
URL_BASE = RESOURCE_CPP_API + "/api/publishers"


class VirtualMachine(Submission):
    """Azure Partner Center Virtual Machine offer."""

    def __init__(
        self,
        name=None,
        notification_emails=None,
        config_yaml=r"config.yml",
        app_path: str = ".",
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
        self._legacy_authorization = None

    def create(self):
        """
        Create Virtual Machine offer

        First,  verify that the offer does not already exist by checking the offer name.
        If the offer is found, this command should fail, and the user should instead try "update".

        The 'Update' command is used to create a new offer when the offer does not exist.
        """
        try:
            if self.show()["id"]:
                raise NameError("Virtual Machine offer already exists. Try using 'update'?")
        except LookupError:
            pass  # Passing this error is the only way to determine that an offer does not exist
        return self.update()

    def update(self):
        """Update Existing Virtual Machine offer"""
        headers, json_config, url = self._prepare_request()

        response = requests.put(url, json=json_config, headers=headers)
        if response.status_code != 200:
            self._raise_connection_error(response)
        return response.json()

    def list_contents(self) -> dict:
        """list only the Virtual Machine offers"""
        with open(self.config_yaml, encoding="utf8") as file:
            settings = yaml.safe_load(file)
            if "publisherId" not in settings:
                raise ValueError(f"Key: publisherId is missing from {self.config_yaml}")
            publisher_id = settings["publisherId"]
        offer_type_filter = "offerTypeId eq 'microsoft-azure-virtualmachines'"
        url = f"{URL_BASE}/{publisher_id}/offers?api-version=2017-10-31&$filter={offer_type_filter}"
        headers = {"Authorization": self.get_auth(RESOURCE_CPP_API), "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()

    def publish(self):
        """Publish Existing Virtual Machine offer"""
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)
        if "publisherId" not in json_config:
            raise ValueError(f"Key: publisherId is missing from {self.app_path}/{self.json_listing_config}")
        publisher_id = json_config["publisherId"]
        offer_id = json_config["id"]

        url = f"{URL_BASE}/{publisher_id}/offers/{offer_id}/publish?api-version=2017-10-31"

        headers = {"Authorization": self.get_auth(RESOURCE_CPP_API), "Content-Type": "application/json"}

        response = requests.post(
            url, json={"metadata": {"notification-emails": self.notification_emails}}, headers=headers
        )
        if response.status_code != 202:
            self._raise_connection_error(response)
        return response

    def get_auth(self, resource=RESOURCE_PC_API) -> str:
        """
        Create Authentication Header

        :return: Authorization Header contents
        """
        if resource == RESOURCE_PC_API:
            if self._authorization is None:
                self._authorization = f"Bearer {self._get_auth(resource)}"
            return self._authorization

        if resource == RESOURCE_CPP_API:
            if self._legacy_authorization is None:
                self._legacy_authorization = f"Bearer {self._get_auth(resource)}"
            return self._legacy_authorization
        raise Exception("The provided resource is unsupported.")

    def _get_auth(self, resource) -> str:
        with open(self.config_yaml, encoding="utf8") as file:
            settings = yaml.safe_load(file)

        client_id = os.getenv(AAD_ID, settings["aad_id"])
        client_secret = os.getenv(AAD_CRED, settings["aad_secret"])
        tenant_id = os.getenv(TENANT_ID, settings["tenant_id"])

        auth_context = AuthenticationContext(f"https://login.microsoftonline.com/{tenant_id}")
        token_response = auth_context.acquire_token_with_client_credentials(
            resource=resource,
            client_id=client_id,
            client_secret=client_secret,
        )
        return token_response["accessToken"]

    def _prepare_request(self):
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)
            if "publisherId" not in json_config:
                raise ValueError(f"Key: publisherId is missing from {self.app_path}/{self.json_listing_config}")
            publisher_id = json_config["publisherId"]
        offer_id = json_config["id"]
        url = f"{URL_BASE}/{publisher_id}/offers/{offer_id}?api-version=2017-10-31"
        headers = {"Authorization": self.get_auth(RESOURCE_CPP_API), "Content-Type": "application/json"}
        return headers, json_config, url

    def _raise_connection_error(self, response):
        """if response body is not provided, return with the error code instead"""
        error_string = (
            json.dumps(response.json(), indent=4).replace("\\r", "").replace("\\n", os.linesep)
            if response.json()
            else response.status_code
        )
        raise ConnectionError(error_string)


class VirtualMachineCLI(CLIParser):
    """Methods for Virtual Machine"""

    def __init__(self):
        super().__init__(submission_type=VirtualMachine)

    def publish(self):
        """Publish a Virtual Machine Offer"""
        args = self._add_name_notification_emails_argument()
        return VirtualMachine(
            args.name,
            notification_emails=args.notification_emails,
            app_path=args.app_path,
            json_listing_config=args.config_json,
            config_yaml=args.config_yml,
        ).publish()
