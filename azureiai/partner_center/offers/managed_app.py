#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Managed Applications"""
from azureiai.managed_apps.utils import CONFIG_YML, APP_NAME
from azureiai.partner_center import OfferParser
from azureiai.partner_center.offer import Offer

AZURE_APPLICATION = "AzureApplication"


class ManagedApp(Offer):
    """Azure Partner Center Managed Application Submission"""

    def __init__(
        self, name=None, config_yaml=CONFIG_YML, app_path: str = APP_NAME, json_listing_config="sample_ma_listing_config.json"
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_APPLICATION,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )


class ManagedAppParser(OfferParser):
    """Managed Application CLI Parser"""

    def __init__(self):
        super().__init__(submission_type=ManagedApp)
