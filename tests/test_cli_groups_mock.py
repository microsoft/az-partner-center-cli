#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest
from pathlib import Path

from tests.cli_groups_tests import (
    vm_list_command,
    ma_list_command,
    vm_create_command,
    vm_show_command,
    ma_create_command,
    ma_show_command,
    ma_delete_command,
    vm_delete_command,
    vm_publish_command,
    ma_publish_command,
    vm_update_command,
    ma_update_command,
)


@pytest.fixture
def config_yml():
    """Fixuture used to configure deployment for testing"""
    test_path = Path(__file__).parents[1]
    config_path = test_path.joinpath("config.yml")
    return config_path if config_path.is_file() else test_path.joinpath("template.config.yml")


def test_vm_list_mock(config_yml, monkeypatch, ama_mock):
    vm_list_command(config_yml, monkeypatch)


def test_vm_create_mock(config_yml, monkeypatch, ama_mock):
    vm_create_command(config_yml, monkeypatch)


def test_vm_update_mock(config_yml, monkeypatch, ama_mock):
    vm_update_command(config_yml, monkeypatch)


def test_vm_show_mock(config_yml, monkeypatch, ama_mock):
    vm_show_command(config_yml, monkeypatch)


def test_vm_publish_mock(config_yml, monkeypatch, ama_mock):
    vm_publish_command(config_yml, monkeypatch)


def test_vm_delete_mock(config_yml, monkeypatch, ama_mock):
    vm_delete_command(config_yml, monkeypatch)


def test_ma_list_mock(config_yml, monkeypatch, ama_mock):
    ma_list_command(config_yml, monkeypatch)


def test_ma_create_mock(config_yml, monkeypatch, ama_mock):
    ma_create_command(config_yml, monkeypatch)


def test_ma_update_mock(config_yml, monkeypatch, ama_mock):
    ma_update_command(config_yml, monkeypatch)


def test_ma_show_mock(config_yml, monkeypatch, ama_mock):
    ma_show_command(config_yml, monkeypatch)


def test_ma_publish_mock(config_yml, monkeypatch, ama_mock):
    ma_publish_command(config_yml, monkeypatch)


def test_ma_delete_mock(config_yml, monkeypatch, ama_mock):
    ma_delete_command(config_yml, monkeypatch)
