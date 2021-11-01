#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Virtual Machines"""
from azureiai.managed_apps.utils import CONFIG_YML
from azureiai.partner_center import OfferParser
from azureiai.partner_center.offer import Offer

AZURE_VIRTUAL_MACHINE = "AzureThirdPartyVirtualMachine"


class VirtualMachine(Offer):
    """Azure Partner Center Virtual Machine offer."""

    def __init__(
        self, name=None, config_yaml=CONFIG_YML, app_path: str = "sample_app", json_listing_config="vm_config.json"
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_VIRTUAL_MACHINE,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )


class VirtualMachineOffer(OfferParser):
    """Methods for Virtual Machine"""

    def __init__(self):
        super().__init__(submission_type=VirtualMachine)
