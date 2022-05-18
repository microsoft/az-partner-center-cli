#   ---------------------------------------------------------
#   Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#   ---------------------------------------------------------
"""
Azure Managed Applications - Status

Get status of existing Azure Managed Applications using the command 'status'.

Example Response
    Published: {"are-resources-ready": True, "state": "Published", "substate": "Ready"}

    Draft: {"are-resources-ready": False, "state": "Not-Submitted", "substate": "Draft"}

    Not Found: {"are-resources-ready": False, "state": "Not-Found", "substate": "Unknown Product Id"}
"""
import argparse

from azureiai.managed_apps import ManagedApplication
from azureiai.managed_apps.commands.common import add_config_yml, add_ama_name, add_command, add_product_id
from swagger_client.models.microsoft_ingestion_api_models_submissions_submission import (
    MicrosoftIngestionApiModelsSubmissionsSubmission,
)
from swagger_client.rest import ApiException


def run():
    """Implementation of run interface for status"""
    parser = argparse.ArgumentParser("Azure Managed Applications - Status")
    add_config_yml(parser)
    add_product_id(parser)
    add_ama_name(parser)
    add_command(parser)

    args = parser.parse_args()
    ama = ManagedApplication(config_yaml=args.config_yml)
    ama.set_product_id(args.product_id)
    try:
        response = ama.submission_status()
        if response.value:
            submission_response: MicrosoftIngestionApiModelsSubmissionsSubmission = response.value[0]
            return {
                "are-resources-ready": submission_response.are_resources_ready,
                "state": submission_response.state,
                "substate": submission_response.substate,
            }
        return {"are-resources-ready": False, "state": "Not-Submitted", "substate": "Draft"}
    except ApiException:
        return {"are-resources-ready": False, "state": "Not-Found", "substate": "Unknown Product Id"}
