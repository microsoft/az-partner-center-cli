#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest
from pathlib import Path

from tests import cli_groups_tests as cli_tests


@pytest.fixture
def config_yml():
    """Fixuture used to configure deployment for testing"""
    test_path = Path(__file__).parents[1]
    config_path = test_path.joinpath("config.yml")
    return config_path if config_path.is_file() else test_path.joinpath("template.config.yml")


@pytest.fixture
def vm_config_json():
    """Fixuture used to configure deployment for testing"""
    test_path = Path(__file__).parents[1]
    config_path = test_path.joinpath("vm_listing_config.json")
    return config_path if config_path.is_file() else test_path.joinpath("template.vm.listing.json")


@pytest.fixture
def ma_config_json():
    """Fixuture used to configure deployment for testing"""
    test_path = Path(__file__).parents[1]
    config_path = test_path.joinpath("ma_config.json")
    return config_path if config_path.is_file() else test_path.joinpath("template.listing_config.json")


@pytest.fixture
def st_config_json():
    """Fixuture used to configure deployment for testing"""
    test_path = Path(__file__).parents[1]
    config_path = test_path.joinpath("st_config.json")
    return config_path if config_path.is_file() else test_path.joinpath("template.listing_config.json")


def test_vm_list_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.vm_list_command(config_yml, monkeypatch)


def test_vm_create_mock(config_yml, vm_config_json, monkeypatch, ama_mock):
    cli_tests.vm_create_command(config_yml, vm_config_json, monkeypatch)


def test_vm_update_mock(config_yml, vm_config_json, monkeypatch, ama_mock):
    cli_tests.vm_update_command(config_yml, vm_config_json, monkeypatch)


def test_vm_show_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.vm_show_command(config_yml, monkeypatch)


def test_vm_publish_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.vm_publish_command(config_yml, monkeypatch)


def test_vm_delete_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.vm_delete_command(config_yml, monkeypatch)


def test_ma_list_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.ma_list_command(config_yml, monkeypatch)


def test_ma_create_mock(config_yml, ma_config_json, monkeypatch, ama_mock):
    cli_tests.ma_create_command(config_yml, ma_config_json, monkeypatch)


def test_ma_update_mock(config_yml, ma_config_json, monkeypatch, ama_mock):
    cli_tests.ma_update_command(config_yml, ma_config_json, monkeypatch)


def test_ma_show_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.ma_show_command(config_yml, monkeypatch)


def test_ma_publish_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.ma_publish_command(config_yml, monkeypatch)


def test_ma_delete_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.ma_delete_command(config_yml, monkeypatch)


def test_st_list_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.st_list_command(config_yml, monkeypatch)


def test_st_create_mock(config_yml, st_config_json, monkeypatch, ama_mock):
    cli_tests.st_create_command(config_yml, st_config_json, monkeypatch)


def test_st_update_mock(config_yml, st_config_json, monkeypatch, ama_mock):
    cli_tests.st_update_command(config_yml, st_config_json, monkeypatch)


def test_st_show_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.st_show_command(config_yml, monkeypatch)


def test_st_publish_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.st_publish_command(config_yml, monkeypatch)


def test_st_delete_mock(config_yml, monkeypatch, ama_mock):
    cli_tests.st_delete_command(config_yml, monkeypatch)
