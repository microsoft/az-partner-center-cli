#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------

import pytest
from azureiai import ama_app
from tests.cli_tests import (
    bad_command_integration,
    create_publish_delete,
    create_publish_publish_delete,
    create_publish_missing_config,
    create_publish_missing_manifest,
    create_then_delete,
    get_status,
    list_command,
    status_check,
    update_ama,
)


@pytest.mark.integration
def test_app():
    with pytest.raises(KeyError):
        ama_app.main()


@pytest.mark.integration
def test_bad_command_integration(monkeypatch):
    bad_command_integration(monkeypatch)


@pytest.mark.integration
def test_list(config_yml, monkeypatch):
    list_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_create_then_delete(config_yml, monkeypatch, manifest_yml):
    create_then_delete(config_yml, monkeypatch, manifest_yml)


@pytest.mark.integration
def test_status_mock(config_yml, manifest_yml, monkeypatch):
    status_check(config_yml, manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_delete(config_yml, manifest_yml, monkeypatch):
    create_publish_delete(config_yml, manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_update_publish_delete(config_yml, manifest_yml, monkeypatch):
    update_ama(config_yml, manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_publish_delete(config_yml, manifest_yml, monkeypatch):
    create_publish_publish_delete(config_yml, manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_missing_config(config_yml, manifest_yml, monkeypatch):
    create_publish_missing_config(config_yml, manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_missing_manifest(config_yml, monkeypatch, manifest_yml):
    create_publish_missing_manifest(config_yml, monkeypatch, manifest_yml)


@pytest.mark.integration
def test_get_status(config_yml, monkeypatch):
    get_status(config_yml, monkeypatch)
