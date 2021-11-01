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


def test_list_mock(config_yml, monkeypatch, ama_mock):
    list_command(config_yml, monkeypatch)


def test_create_then_delete_mock(config_yml, monkeypatch, manifest_yml, ama_mock):
    create_then_delete(config_yml, monkeypatch, manifest_yml)


def test_create_update_delete_mock(config_yml, manifest_yml, monkeypatch, ama_mock):
    update_ama(config_yml, manifest_yml, monkeypatch)


def test_create_publish_delete_mock(config_yml, manifest_yml, monkeypatch, ama_mock):
    create_publish_delete(config_yml, manifest_yml, monkeypatch)


def test_status_mock(config_yml, manifest_yml, monkeypatch, ama_mock):
    status_check(config_yml, manifest_yml, monkeypatch)


def test_create_publish_missing_config_mock(config_yml, manifest_yml, monkeypatch, ama_mock):
    create_publish_missing_config(config_yml, manifest_yml, monkeypatch)


def test_create_publish_missing_manifest_mock(config_yml, monkeypatch, ama_mock, manifest_yml):
    create_publish_missing_manifest(config_yml, monkeypatch, manifest_yml)
