#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Azure Managed Applications - Delete

Delete an existing Azure Managed Application using the command 'delete'.
"""
import argparse

from azureiai.managed_apps import ManagedApplication
from azureiai.managed_apps.commands.common import add_config_yml, add_command, add_product_id


def run():
    """Implementation of Run Interface for delete"""
    parser = argparse.ArgumentParser("Azure Managed Applications - Delete")
    add_config_yml(parser)
    add_product_id(parser)
    add_command(parser)

    args = parser.parse_args()
    ama = ManagedApplication(config_yaml=args.config_yml)
    ama.set_product_id(args.product_id)
    ama.delete()
    output = {"deleted": True}
    return output
