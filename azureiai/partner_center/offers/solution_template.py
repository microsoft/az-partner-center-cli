#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Solution Templates"""
from azureiai.managed_apps.utils import CONFIG_YML
from azureiai.partner_center import OfferParser
from azureiai.partner_center.offer import Offer

AZURE_APPLICATION = "AzureApplication"


class SolutionTemplate(Offer):
    """Azure Partner Center Managed Application Submission"""

    def __init__(
        self, name=None, config_yaml=CONFIG_YML, app_path: str = "sample_app", json_listing_config="sample_app_listing_config.json"
    ):
        super().__init__(
            name=name,
            config_yaml=config_yaml,
            resource_type=AZURE_APPLICATION,
            app_path=app_path,
            json_listing_config=json_listing_config,
        )


class SolutionTemplateParser(OfferParser):
    """Methods for Solution Template"""

    def __init__(self):
        super().__init__(submission_type=SolutionTemplate)
