#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Virtual Machines"""
import json
from pathlib import Path

import requests
import yaml

from azureiai.managed_apps.utils import CONFIG_YML
from azureiai.partner_center import OfferParser
from azureiai.partner_center.offer import Offer

AZURE_VIRTUAL_MACHINE = "AzureThirdPartyVirtualMachine"


class VirtualMachine(Offer):
    """Azure Partner Center Virtual Machine offer."""

    def __init__(
        self, name=None, config_yaml=CONFIG_YML, app_path: str = "sample_app", json_listing_config="sample_app_listing_config.json"
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_VIRTUAL_MACHINE,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )

    def update(self):
        """Update Existing Application"""
        return self._set_win_vm_offer()

    def create(self):
        """Create new Azure Submission and set product id."""
        return self.update()

    def _set_win_vm_offer(self):
        with open(Path(self.app_path).joinpath(self.json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        mam = "microsoft-azure-marketplace"
        ma_vm = "microsoft-azure-virtualmachines"

        offer_type_versions_vm = 1
        offer_type_versions_marketplace = 1

        os_vhd_url = "http://contosoteststorage.blob.core.windows.net/test/contosoVM.vhd?sv=2014-02-14&sr=c&sig=WlDo6Q4xwYH%2B5QEJbItPUVdgHhBcrVxPBmntZ2vU96w%3D&st=2016-06-25T18%3A30%3A00Z&se=2017-06-25T18%3A30%3A00Z&sp=rl"
        small_logo = "https://publishingapistore.blob.core.windows.net/testcontent/D6191_publishers_contoso/contosovirtualmachine/6218c455-9cbc-450c-9920-f2e7a69ee132.png?sv=2014-02-14&sr=b&sig=6O8MM9dgiJ48VK0MwddkyVbprRAnBszyhVkVHGShhkI%3D&se=2019-03-28T19%3A46%3A50Z&sp=r"
        medium_logo = "https://publishingapistore.blob.core.windows.net/testcontent/D6191_publishers_contoso/contosovirtualmachine/557e714b-2f31-4e12-b0cc-e48dd840edf4.png?sv=2014-02-14&sr=b&sig=NwL67NTQf9Gc9VScmZehtbHXpYmxhwZc2foy3o4xavs%3D&se=2019-03-28T19%3A46%3A49Z&sp=r"
        large_logo = "https://publishingapistore.blob.core.windows.net/testcontent/D6191_publishers_contoso/contosovirtualmachine/142485da-784c-44cb-9523-d4f396446258.png?sv=2014-02-14&sr=b&sig=xaMxhwx%2FlKYfz33mJGIg8UBdVpsOwVvqhjTJ883o0iY%3D&se=2019-03-28T19%3A46%3A49Z&sp=r"
        wide_logo = "https://publishingapistore.blob.core.windows.net/testcontent/D6191_publishers_contoso/contosovirtualmachine/48af9013-1df7-4c94-8da8-4626e5039ce0.png?sv=2014-02-14&sr=b&sig=%2BnN7f2tprkrqb45ID6JlT01zXcy1PMTkWXtLKD6nfoE%3D&se=2019-03-28T19%3A46%3A49Z&sp=r"
        hero_logo = "https://publishingapistore.blob.core.windows.net/testcontent/D6191_publishers_contoso/contosovirtualmachine/c46ec74d-d214-4fb5-9082-3cee55200eba.png?sv=2014-02-14&sr=b&sig=RfDvjowFGpP4WZGAHylbF2CuXwO2NXOrwycrXEJvJI4%3D&se=2019-03-28T19%3A46%3A49Z&sp=r"

        plan_0 = {
            "planId": json_config["plan_overview"][0]["plan_listing"]["title"],
            f"{ma_vm}.skuTitle": json_config["plan_overview"][0]["plan_listing"]["title"],
            f"{ma_vm}.skuSummary": json_config["plan_overview"][0]["plan_listing"]["summary"],
            f"{ma_vm}.skuDescription": json_config["plan_overview"][0]["plan_listing"][
                "description"
            ],
            f"{ma_vm}.hideSKUForSolutionTemplate": False,
            f"{ma_vm}.cloudAvailability": ["PublicAzure"],
            "virtualMachinePricing": {"isByol": False, "freeTrialDurationInMonths": 0},
            f"{ma_vm}.operatingSystemFamily": "Windows",
            f"{ma_vm}.windowsOSType": "Other",
            f"{ma_vm}.operationSystem": "WinS2019",
            f"{ma_vm}.recommendedVMSizes": [
                "a0-basic",
                "a0-standard",
                "a1-basic",
                "a1-standard",
                "a2-basic",
                "a2-standard",
            ],
            f"{ma_vm}.openPorts": [],
            f"{ma_vm}.vmImages": {
                json_config["plan_overview"][0]["technical_configuration"]["version"]: {
                    "osVhdUrl": os_vhd_url,
                    "lunVhdDetails": [],
                }
            },
            "regions": ["AZ"],
        }

        body = {
            "publisherId": json_config["offer_listing"]["publisher_name"],
            "offerTypeId": ma_vm,
            "id": json_config["offer_setup"]["alias"],
            "offerTypeVersions": {
                ma_vm: offer_type_versions_vm,
                mam: offer_type_versions_marketplace,
            },
            "definition": {
                "displayText": json_config["offer_listing"]["title"],
                "offer": {
                    f"{mam}.title": json_config["offer_listing"]["title"],
                    f"{mam}.summary": json_config["offer_listing"]["summary"],
                    f"{mam}.longSummary": json_config["offer_listing"]["description"],
                    f"{mam}.description": json_config["offer_listing"]["short_description"],
                    f"{mam}.offerMarketingUrlIdentifier": json_config["offer_setup"]["alias"],
                    f"{mam}.allowedSubscriptions": json_config["preview_audience"]["subscriptions"],
                    f"{mam}.smallLogo": small_logo,
                    f"{mam}.mediumLogo": medium_logo,
                    f"{mam}.largeLogo": large_logo,
                    f"{mam}.wideLogo": wide_logo,
                    f"{mam}.heroLogo": hero_logo,
                    f"{mam}.screenshots": [],
                    f"{mam}.videos": [],
                    f"{mam}.leadDestination": "None",
                    f"{mam}.privacyURL": json_config["offer_listing"]["listing_uris"][0]["uri"],
                    f"{mam}.termsOfUse": "Terms of use",
                    f"{mam}.engineeringContactName": json_config["offer_listing"]["listing_contacts"][1]["name"],
                    f"{mam}.engineeringContactEmail": json_config["offer_listing"]["listing_contacts"][1]["email"],
                    f"{mam}.engineeringContactPhone": json_config["offer_listing"]["listing_contacts"][1]["phone"],
                    f"{mam}.supportContactName": json_config["offer_listing"]["listing_contacts"][0]["name"],
                    f"{mam}.supportContactEmail": json_config["offer_listing"]["listing_contacts"][0]["email"],
                    f"{mam}.supportContactPhone": json_config["offer_listing"]["listing_contacts"][0]["email"],
                    f"{mam}.publicAzureSupportUrl": json_config["offer_listing"]["listing_uris"][1]["uri"],
                    f"{mam}.fairfaxSupportUrl": "",
                    f"{mam}.usefulLinks": [
                        {"linkTitle": "Contoso App for Azure", "linkUrl": "https://azuremarketplace.microsoft.com"}
                    ],
                    f"{mam}.categoryMap": [
                        {"categoryL1": "analytics", "categoryL2-analytics": ["visualization-and-reporting"]},
                        {
                            "categoryL1": "ai-plus-machine-learning",
                            "categoryL2-ai-plus-machine-learning": ["bot-services", "cognitive-services", "other"],
                        },
                    ],
                },
                "plans": [plan_0],
            },
            "eTag": "W/\"datetime'2017-06-07T06%3A15%3A40.4771399Z'\"",
            "version": 5,
        }

        resource_path = f'https://cloudpartner.azure.com/api/publishers/microsoftcorporation1590077852919/offers/test_vm?api-version=2017-10-31'

        with open(self.config_yaml, encoding="utf8") as file:
            settings = yaml.safe_load(file)

        client_id = settings["aad_id"]
        client_secret = settings["aad_secret"]
        tenant_id = settings["tenant_id"]
        from adal import AuthenticationContext
        auth_context = AuthenticationContext(f"https://login.microsoftonline.com/{tenant_id}")
        token = auth_context.acquire_token_with_client_credentials(
            resource="https://cloudpartner.azure.com",
            client_id=client_id,
            client_secret=client_secret,
        )

        headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {token['accessToken']}"}
        response = requests.put(url=resource_path, json=body, headers=headers)

        if response.status_code != 200:
            raise Exception(response.text)
        return response


class VirtualMachineOffer(OfferParser):
    """Methods for Virtual Machine"""

    def __init__(self):
        super().__init__(submission_type=VirtualMachine)
