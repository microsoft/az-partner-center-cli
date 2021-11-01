#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Azure Managed Applications - Publish

Publish an existing Azure Managed Application using the command 'publish'.
"""
import argparse

from azureiai.managed_apps.commands.common import _load_ama


def run():
    """Implementation of run interface for publish"""
    parser = argparse.ArgumentParser("Azure Managed Applications - Publish")
    ama, _, _, args = _load_ama(parser)

    response = ama.publish()

    url = "https://partner.microsoft.com/en-us/dashboard/commercial-marketplace/offers/%s/overview" % args.product_id
    output = {"response": response, "url": url, "plan_id": ama.get_plan_id()}

    return output
