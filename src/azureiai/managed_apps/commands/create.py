#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Azure Managed Application - Create

Create a new Azure Managed Application using the command 'create'.
"""
import argparse
import os

from azureiai.managed_apps import ManagedApplication
from azureiai.managed_apps.commands.common import add_config_yml, add_ama_name, add_command, add_manifest_yml


def run():
    """Implementation of Run Interface for create"""
    parser = argparse.ArgumentParser("Azure Managed Applications - Create")
    add_command(parser)
    add_ama_name(parser)
    add_config_yml(parser)
    add_manifest_yml(parser)

    args = parser.parse_args()
    ama_name = args.ama_name
    config_yml = args.config_yml
    ama = ManagedApplication(ama_name, config_yaml=config_yml)
    ama.create()
    manifest_yml = args.manifest_yml
    if not os.path.isfile(manifest_yml):
        raise FileNotFoundError("Manifest File not found: ", manifest_yml)
    prepared = ama.manifest_publish(manifest_yml=manifest_yml, config_yml=config_yml)

    output = {
        "ama_name": ama_name,
        "product_id": ama.get_product_id(),
        "offer_id": ama.get_offer_id(),
        "prepared": prepared,
        "plan_id": ama.get_plan_id(),
    }
    return output
