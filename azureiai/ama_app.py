#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
This 'main' method has been replaced with the 'main' found in 'az_app.py'. These methods may not be kept up to date.
They are currently kept for test coverage against APIs.

CLI Wrapper for Creating, Updating, or Deleting Azure Managed Applications
"""
import argparse
import json

from azureiai.managed_apps.commands import (
    create,
    delete,
    list as list_command,
    publish,
    status,
    update,
)


def main():
    """CLI Application"""
    parser = argparse.ArgumentParser("Azure Managed Applications - Python SDK")
    parser.add_argument("command", type=str, help="Which command to run")

    args, _ = parser.parse_known_args()

    commands = {
        "create": create.run,
        "delete": delete.run,
        "list": list_command.run,
        "publish": publish.run,
        "status": status.run,
        "update": update.run,
    }

    output = commands[args.command]()
    json_output = json.dumps(output, default=lambda x: hasattr(x, "__dict__") if x.__dict__ else x)
    return json_output
