#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Azure Managed Applications - Publish

Publish an existing Azure Managed Application using the command 'publish'.
"""
import argparse
import os

from azureiai.managed_apps import ManagedApplication
from azureiai.managed_apps.commands import (
    add_ama_name,
    add_command,
    add_config_yml,
    add_manifest_yml,
    add_product_id,
)


def run():
    """Implementation of run interface for publish"""
    parser = argparse.ArgumentParser("Azure Managed Applications - Publish")
    add_command(parser)
    add_ama_name(parser)
    add_product_id(parser)
    add_config_yml(parser)
    add_manifest_yml(parser)

    args = parser.parse_args()
    config_yml = args.config_yml
    if not os.path.isfile(config_yml):
        raise FileNotFoundError("Configuration File not found!")
    ama = ManagedApplication(name=args.ama_name, config_yaml=config_yml)
    ama.set_product_id(args.product_id)
    manifest_yml = args.manifest_yml
    if not os.path.isfile(manifest_yml):
        raise FileNotFoundError("Manifest File not found: ", manifest_yml)
    prepared = ama.manifest_publish(manifest_yml=manifest_yml, config_yml=config_yml)
    response = None
    if prepared:
        response = ama.publish()

    url = "https://partner.microsoft.com/en-us/dashboard/commercial-marketplace/offers/%s/overview" % args.product_id
    output = {"prepared": prepared, "response": response, "url": url, "plan_id": ama.get_plan_id()}

    return output
