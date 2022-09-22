#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Managed Applications"""
import json
import sys

from azureiai.partner_center.cli_parser import CLIParser
from azureiai.partner_center.plan import PlanCLIParser


def run(submission: CLIParser):
    """CLI Application"""
    subgroup = sys.argv[1]
    command = sys.argv[2]
    help_text = f"""
    Group:
        azpc {subgroup}: Manage Partner Center submissions.

    Subgroups:
        plan    : Application Plan

    Commands:
        list    : list Applications
        create  : create Application
        show    : show Application
        update  : update Application
        delete  : delete Application
        publish : publish Application
        release : release Application
        status  : status Application"""
    if command in ["--help", "-h"]:
        return help_text

    commands = {
        "create": submission.create,
        "delete": submission.delete,
        "list": submission.list_command,
        "publish": submission.publish,
        "status": submission.status,
        "show": submission.show,
        "update": submission.update,
        "release": submission.release,
        "plan": run_plan,
    }
    output = commands[command]()
    return json.dumps(output, default=lambda x: hasattr(x, "__dict__") if x.__dict__ else x, indent=4)


def run_plan():
    """CLI Application"""
    subgroup = sys.argv[1]
    command = sys.argv[2]
    plan_command = sys.argv[3]
    help_text = f"""
    Group:
        azpc {subgroup} {command}: Manage Partner Center Plan submissions.

    Commands:
        list    : list Application Plans
        create  : create Application Plan
        show    : show Application Plan
        update  : update Application Plan
        delete  : delete Application Plan
        publish : publish Application Plan
"""
    if plan_command in ["--help", "-h"]:
        return help_text

    plan = PlanCLIParser()
    commands = {
        "create": plan.create,
        "delete": plan.delete,
        "list": plan.list_command,
        "publish": plan.publish,
        "show": plan.show,
        "update": plan.update,
    }

    return commands[plan_command]()
