#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Virtual Machines"""
from azureiai.partner_center.cli_parser import CLIParser
from azureiai.partner_center.submission import Submission

AZURE_VIRTUAL_MACHINE = "AzureThirdPartyVirtualMachine"


class VirtualMachine(Submission):
    """Azure Partner Center Virtual Machine offer."""

    def __init__(
        self, name=None, config_yaml=r"config.yml", app_path: str = "sample_app", json_listing_config="vm_config.json"
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_VIRTUAL_MACHINE,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )


class VirtualMachineCLI(CLIParser):
    """Methods for Virtual Machine"""

    def __init__(self):
        super().__init__(submission_type=VirtualMachine)
