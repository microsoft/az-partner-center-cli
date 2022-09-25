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
def test_list(monkeypatch):
    list_command(monkeypatch)


@pytest.mark.integration
def test_create_then_delete(monkeypatch, manifest_yml):
    create_then_delete(monkeypatch, manifest_yml)


@pytest.mark.integration
def test_status_mock(manifest_yml, monkeypatch):
    status_check(manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_delete(manifest_yml, monkeypatch):
    create_publish_delete(manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_update_publish_delete(manifest_yml, monkeypatch):
    update_ama(manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_publish_delete(manifest_yml, monkeypatch):
    create_publish_publish_delete(manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_missing_config(manifest_yml, monkeypatch):
    create_publish_missing_config(manifest_yml, monkeypatch)


@pytest.mark.integration
def test_create_publish_missing_manifest(monkeypatch, manifest_yml):
    create_publish_missing_manifest(monkeypatch, manifest_yml)


@pytest.mark.integration
def test_get_status(monkeypatch):
    get_status(monkeypatch)
