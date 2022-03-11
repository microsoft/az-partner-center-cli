#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Managed Applications"""

import sys

from azureiai.partner_center import run
from azureiai.partner_center.offers.container import ContainerCLI
from azureiai.partner_center.offers.managed_app import ManagedAppCLI
from azureiai.partner_center.offers.solution_template import SolutionTemplateCLI
from azureiai.partner_center.offers.virtual_machine import VirtualMachineCLI


def main():
    """CLI Application"""
    help_text = """
    Group:
        azpc : Manage Partner Center submissions.

    Subgroups:
        ma       : Managed Applications
        st       : Solution Templates
        vm       : Virtual Machine Images
        co       : Containers
"""
    subgroup = sys.argv[1]
    if subgroup in ["--help", "-h"]:
        return help_text

    commands = {
        "ma": ManagedAppCLI,
        "vm": VirtualMachineCLI,
        "st": SolutionTemplateCLI,
        "co": ContainerCLI,
    }
    return run(commands[subgroup]())


if __name__ == "__main__":
    main()
