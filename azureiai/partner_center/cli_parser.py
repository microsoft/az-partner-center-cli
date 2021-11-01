#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Partner Center Submissions"""
import argparse

from azureiai.partner_center.submission import Submission


class CLIParser:
    """Interface for Submission Types"""

    def __init__(self, submission_type=Submission):
        self.parser = argparse.ArgumentParser("azpc")
        self.parser.add_argument("subgroup", type=str, help="Which subgroup to run")
        self.parser.add_argument("command", type=str, help="Which command to run")
        self.submission_type = submission_type

        self._name = "--name"

    def create(self) -> {}:
        """Create a new Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name).create()

    def delete(self) -> {}:
        """Delete a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name).delete()

    def list_command(self) -> {}:
        """List Managed Applications"""
        return self.submission_type().list_contents()

    def publish(self) -> {}:
        """Publish a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name).publish()

    def show(self) -> {}:
        """Show a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name).show()

    def update(self) -> {}:
        """Update a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name).update()

    def _add_name_argument(self):
        self.parser.add_argument(self._name, type=str, help="Managed App Name")
        args = self.parser.parse_args()
        return args
