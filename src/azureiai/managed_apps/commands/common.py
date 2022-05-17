#   ---------------------------------------------------------
#   Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#   ---------------------------------------------------------
"""
Helper Commands for CLI

Use add parser argument methods to build arg parser for new commands.
"""
import os
from argparse import ArgumentParser

from azureiai.managed_apps import ManagedApplication


def add_image_toggle(parser: ArgumentParser):
    """
    Add Configuration Setting to Arg Parser

    :param parser: ArgumentParser from CLI Main Method
    """
    parser.add_argument("--update-image", type=bool, help="Update Images", default=False)


def add_config_yml(parser: ArgumentParser):
    """
    Add Configuration Setting to Arg Parser

    :param parser: ArgumentParser from CLI Main Method
    """
    parser.add_argument("--config-yml", type=str, help="Configuration YML", default="config.yml")


def add_ama_name(parser: ArgumentParser):
    """
    Add Azure Managed Application Name to Arg Parser

    :param parser: ArgumentParser from CLI Main Method
    """
    parser.add_argument("--ama-name", type=str, help="Managed App Name", default="default_name")


def add_command(parser: ArgumentParser):
    """
    Add Command to Arg Parser

    :param parser: ArgumentParser from CLI Main Method
    """
    parser.add_argument("command", type=str, help="Which command to run")


def add_product_id(parser: ArgumentParser):
    """
    Add Product ID to Arg Parser

    :param parser: ArgumentParser from CLI Main Method
    """
    parser.add_argument("--product-id", type=str, help="Product ID")


def add_offer_id(parser: ArgumentParser):
    """
    Add Offer ID to Arg Parser

    :param parser: ArgumentParser from CLI Main Method
    """
    parser.add_argument("--offer-id", type=str, help="Offer ID")


def add_manifest_yml(parser: ArgumentParser):
    """
    Add Manifest YML to Arg Parser

    :param parser: ArgumentParser from CLI Main Method
    """
    parser.add_argument(
        "--manifest-yml",
        type=str,
        help="Manifest YML with file paths",
        default="manifest.yml",
    )


def _load_ama(parser):
    add_command(parser)
    add_ama_name(parser)
    add_product_id(parser)
    add_config_yml(parser)
    add_manifest_yml(parser)
    add_offer_id(parser)
    args = parser.parse_args()
    config_yml = args.config_yml
    if not os.path.isfile(config_yml):
        raise FileNotFoundError("Configuration File not found!")
    ama = ManagedApplication(name=args.ama_name, config_yaml=config_yml)
    ama.set_product_id(args.product_id)
    if "offer_id" in args:
        ama.set_offer_id(args.offer_id)
    manifest_yml = args.manifest_yml
    if not os.path.isfile(manifest_yml):
        raise FileNotFoundError("Manifest File not found: ", manifest_yml)
    return ama, config_yml, manifest_yml, args
