#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI Wrapper for Creating, Updating, or Deleting Azure Partner Center Submissions"""
import argparse
from distutils.util import strtobool

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
        self._app_path = "--app-path"

    def create(self) -> dict:
        """Create a new Application"""
        self.parser.add_argument(
            "--update",
            help="Update App if it exists.",
            type=lambda x: bool(strtobool(x)),
            nargs="?",
            const=True,
            default=False,
        )
        args = self._add_name_config_json_argument()
        try:
            return self.submission_type(
                args.name, config_yaml=args.config_yml, app_path=args.app_path, json_listing_config=args.config_json
            ).create()
        except NameError as error:
            if hasattr(args, "update"):
                return self._update(args)
            raise error

    def delete(self) -> dict:
        """Delete a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml).delete()

    def list_command(self) -> dict:
        """List Managed Applications"""
        args = self.parser.parse_args()
        return self.submission_type(config_yaml=args.config_yml).list_contents()

    def publish(self) -> dict:
        """Publish a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml).publish()

    def release(self) -> dict:
        """Release a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml).release()

    def show(self) -> dict:
        """Show a Managed Application"""
        args = self._add_name_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml).show()

    def update(self) -> dict:
        """Update a Managed Application"""
        args = self._add_name_config_json_argument()
        return self._update(args)

    def _update(self, args):
        return self.submission_type(
            args.name, config_yaml=args.config_yml, app_path=args.app_path, json_listing_config=args.config_json
        ).update()

    def status(self) -> dict:
        """Get the Status of an offer"""
        args = self._add_name_argument()
        return self.submission_type(args.name, config_yaml=args.config_yml).status()

    def _add_name_argument(self):
        self.parser.add_argument(self._name, type=str, help="Managed App Name")
        args = self.parser.parse_args()
        return args

    def _add_name_config_json_argument(self):
        self.parser.add_argument(self._name, type=str, help="Managed App Name")
        self.parser.add_argument(
            self._config_json, type=str, help="Listing Configuration Json", default="listing_config.json"
        )
        self.parser.add_argument(self._app_path, type=str, help="Application Root Directory", default=".")
        args = self.parser.parse_args()
        return args

    def _add_name_notification_emails_argument(self):
        self.parser.add_argument(self._name, type=str, required=True, help="Managed App Name")
        self.parser.add_argument(
            self._notification_emails, type=str, required=True, help="Notification e-mails to use when publishing"
        )

        self.parser.add_argument(
            self._config_json, type=str, help="Listing Configuration Json", default="listing_config.json"
        )
        self.parser.add_argument(self._app_path, type=str, help="Application Root Directory", default=".")
        args = self.parser.parse_args()
        return args
