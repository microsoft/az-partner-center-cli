#   ---------------------------------------------------------
#   Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#   ---------------------------------------------------------
"""
Helper Commands for CLI

Use add parser argument methods to build arg parser for new commands.
"""
from argparse import ArgumentParser


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
