import argparse
import sys


def setup_patched_app(monkeypatch, input_args):
    def get_args(self, args=None, namespace=None):
        return argparse.Namespace(**input_args)

    def get_known_args(self, args=None, namespace=None):
        return get_args(self, args=args, namespace=namespace), argparse.Namespace()

    monkeypatch.setattr(argparse.ArgumentParser, "parse_known_args", get_known_args)
    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", get_args)

    monkeypatch.setattr(sys, "argv", [""] + list(input_args.values()))
