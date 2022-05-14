#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
from azureiai.partner_center.offers.virtual_machine import VirtualMachineCLI

APP_CLI = VirtualMachineCLI


def list():
    return APP_CLI().list_command()


def get():
    return APP_CLI().show()


def create():
    return APP_CLI().create()


def update():
    return APP_CLI().update()


def begin_delete():
    return APP_CLI().delete()
