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
        self.parser.add_argument("--config-yml", type=str, help="Configuration YML", default="config.yml")
        self.parser.add_argument(
            "--manifest-yml",
            type=str,
            help="Manifest YML with file paths",
            default="manifest.yml",
        )

        self.submission_type = submission_type

        self._name = "--name"
        self._notification_emails = "--notification-emails"
        self._config_json = "--config-json"

    def create(self) -> {}:
        """Create a new Managed Application"""
        args = self._add_name_config_json_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml, json_listing_config=args.config_json).create()

    def delete(self) -> {}:
        """Delete a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml).delete()

    def list_command(self) -> {}:
        """List Managed Applications"""
        return self.submission_type(config_yaml=args.config_yml).list_contents()

    def publish(self) -> {}:
        """Publish a Managed Application"""
        if "VirtualMachine" not in str(self.submission_type):
            args = self._add_name_argument()
            return self.submission_type(args.name, config_yaml=args.config_yml).publish()
        args = self._add_name_notification_emails_argument()
        return self.submission_type(args.name, args.notification_emails, config_yaml=args.config_yml).publish()

    def show(self) -> {}:
        """Show a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml).show()

    def update(self) -> {}:
        """Update a Managed Application"""
        args = self._add_name_config_json_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml, json_listing_config=args.config_json).update()

    def status(self) -> {}:
        """Get the Status of an offer"""
        args = self._add_name_argument()
        return self.submission_type(args.name,  config_yaml=args.config_yml).status()

    def _add_name_argument(self):
        self.parser.add_argument(self._name, type=str, help="Managed App Name")
        args = self.parser.parse_args()
        return args

    def _add_name_config_json_argument(self):
        self.parser.add_argument(self._name, type=str, help="Managed App Name")
        self.parser.add_argument(self._config_json, type=str, help="Listing Configuration Json")
        args = self.parser.parse_args()
        return args

    def _add_name_notification_emails_argument(self):
        self.parser.add_argument(self._name, type=str, required=True, help="Managed App Name")
        self.parser.add_argument(
            self._notification_emails, type=str, required=True, help="Notification e-mails to use when publishing"
        )
        args = self.parser.parse_args()
        return args
