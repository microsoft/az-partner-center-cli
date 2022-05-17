#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Managed Applications"""
from azureiai.partner_center.cli_parser import CLIParser
from azureiai.partner_center.submission import Submission

AZURE_APPLICATION = "AzureApplication"


class ManagedApp(Submission):
    """Azure Partner Center Managed Application Submission"""

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
            resource_type=AZURE_APPLICATION,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )


class ManagedAppCLI(CLIParser):
    """Managed Application CLI Parser"""

    def __init__(self):
        super().__init__(submission_type=ManagedApp)
