#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Solution Templates"""
from azure.partner_center.cli_parser import CLIParser
from azure.partner_center.submission import Submission

AZURE_CONTAINER = "AzureContainer"


class Container(Submission):
    """Azure Partner Center Managed Application Submission"""

    def __init__(
        self,
        name=None,
        app_path: str = ".",
        json_listing_config="ma_config.json",
    ):
        super().__init__(
            name=name,
            resource_type=AZURE_CONTAINER,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )


class ContainerCLI(CLIParser):
    """Methods for Solution Template"""

    def __init__(self):
        super().__init__(submission_type=Container)