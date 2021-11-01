#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Azure Managed Applications - Update

Update an existing Azure Managed Application using the command 'update'.
"""
import argparse

import yaml

from azureiai.managed_apps.commands.common import add_image_toggle, _load_ama


def run():
    """Implementation of run interface for update"""
    parser = argparse.ArgumentParser("Azure Managed Applications - Update")
    add_image_toggle(parser)
    ama, config_yml, manifest_yml, args = _load_ama(parser)

    with open(manifest_yml, encoding="utf8") as file:
        manifest = yaml.safe_load(file)

    response = ama.update(
        app_path=manifest["app_path"],
        app=manifest["app"],
        json_listing_config=manifest["json_listing_config"],
        config_yml=config_yml,
        update_image=True,
    )
    url = "https://partner.microsoft.com/en-us/dashboard/commercial-marketplace/offers/%s/overview" % args.product_id
    output = {
        "ama-name": args.ama_name,
        "product-id": args.product_id,
        "offer-id": args.offer_id,
        "response": response,
        "url": url,
    }

    return output
