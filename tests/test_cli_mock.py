#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest
from azureiai import ama_app
from tests.cli_tests import (
    bad_command_integration,
    create_publish_delete,
    create_publish_missing_config,
    create_publish_missing_manifest,
    create_then_delete,
    list_command,
    status_check,
    update_ama,
)


def test_app():
    with pytest.raises(KeyError):
        ama_app.main()


def test_bad_command(monkeypatch):
    bad_command_integration(monkeypatch)


def test_list_mock(monkeypatch, ama_mock):
    list_command(monkeypatch)


def test_create_then_delete_mock(monkeypatch, manifest_yml, ama_mock):
    create_then_delete(monkeypatch, manifest_yml)


def test_create_update_delete_mock(manifest_yml, monkeypatch, ama_mock):
    update_ama(manifest_yml, monkeypatch)


def test_create_publish_delete_mock(manifest_yml, monkeypatch, ama_mock):
    create_publish_delete(manifest_yml, monkeypatch)


def test_status_mock(manifest_yml, monkeypatch, ama_mock):
    status_check(manifest_yml, monkeypatch)


def test_create_publish_missing_config_mock(manifest_yml, monkeypatch, ama_mock):
    create_publish_missing_config(manifest_yml, monkeypatch)


def test_create_publish_missing_manifest_mock(monkeypatch, ama_mock, manifest_yml):
    create_publish_missing_manifest(monkeypatch, manifest_yml)
