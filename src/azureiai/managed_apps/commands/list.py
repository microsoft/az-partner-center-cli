#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Azure Managed Applications - List

List  existing Azure Managed Applications using the command 'list'.
"""
import argparse

from azureiai.managed_apps import ManagedApplication
from azureiai.managed_apps.commands.common import add_config_yml, add_command


def run():
    """Implementation of run interface for list"""
    parser = argparse.ArgumentParser("Azure Managed Applications - List")
    add_command(parser)
    add_config_yml(parser)

    args = parser.parse_args()
    config_yml = args.config_yml
    ama = ManagedApplication(config_yaml=config_yml)
    offers = ama.get_offers()
    return offers
