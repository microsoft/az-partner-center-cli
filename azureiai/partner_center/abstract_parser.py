import argparse
from abc import ABCMeta, abstractmethod

from azureiai.partner_center.abstract_offer import AbstractOffer


class AbstractParser(metaclass=ABCMeta):
    def __init__(self, submission_type=AbstractOffer):
        self.parser = argparse.ArgumentParser("azpc")
        self.parser.add_argument("subgroup", type=str, help="Which subgroup to run")
        self.parser.add_argument("command", type=str, help="Which command to run")
        self.submission_type = submission_type

        self._name = "--name"

    @abstractmethod
    def create(self):
        """Create a new Managed Application"""
        pass

    @abstractmethod
    def delete(self):
        """Delete a Managed Application"""
        pass

    @abstractmethod
    def list_command(self):
        """List Managed Applications"""
        pass

    @abstractmethod
    def _add_name_argument(self):
        pass

    @abstractmethod
    def publish(self):
        """Publish a Managed Application"""
        pass

    @abstractmethod
    def show(self):
        """Show a Managed Application"""
        pass

    @abstractmethod
    def update(self):
        """Update a Managed Application"""
        pass

    @abstractmethod
    def release(self):
        """Release a Managed Application"""
