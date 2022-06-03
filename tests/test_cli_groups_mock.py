#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest
import json
from pathlib import Path
from adal import AuthenticationContext

from tests import cli_groups_tests as cli_tests

import requests


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


def test_vm_create_mock(config_yml, vm_config_json, monkeypatch):
    vm_config_json = "vm_config.json"
    app_path_fix = "tests/sample_app"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    # Mock creation VM offer API endpoint
    # Set up Requests mock class
    class MockResponse:
        def __init__(self):
            self.status_code = 200

        @staticmethod
        def json():
            with open(Path("tests/test_data/vm_show_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    mock_url = "https://cloudpartner.azure.com/api/publishers/industry-isv-eng/offers/test-vm?api-version=2017-10-31"

    def mock_create_offer(self, headers, json={}, url=mock_url):
        return MockResponse()

    monkeypatch.setattr(requests, "put", mock_create_offer)
    offer_response = cli_tests.vm_create_command(config_yml, vm_config_json, monkeypatch)

    offer = json.loads(offer_response)
    with open(Path(app_path_fix).joinpath(vm_config_json), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    cli_tests._assert_vm_properties(offer, json_config)
    cli_tests._assert_vm_offer_listing(offer, json_config)
    cli_tests._assert_vm_preview_audience(offer, json_config)
    cli_tests._assert_vm_plan_listing(offer, json_config)


def test_vm_update_mock(config_yml, vm_config_json, monkeypatch, ama_mock):
    cli_tests.vm_update_command(config_yml, vm_config_json, monkeypatch)


def test_vm_show_mock(config_yml, vm_config_json, monkeypatch):
    vm_config_json = "vm_config.json"
    app_path_fix = "tests/sample_app"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    # Mock VM offer API endpoint
    # Set up Requests mock class
    class MockResponse:
        def __init__(self):
            self.status_code = 200

        @staticmethod
        def json():
            with open(Path("tests/test_data/vm_show_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    mock_url = "https://cloudpartner.azure.com/api/publishers/industry-isv-eng/offers/test-vm?api-version=2017-10-31"

    def mock_show_offer(self, headers, url=mock_url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_show_offer)

    offer_response = cli_tests.vm_show_command(config_yml, vm_config_json, monkeypatch)

    # Load mocked API JSON response
    offer_listing = json.loads(offer_response)

    # Load JSON config file for assertions
    with open(Path(app_path_fix).joinpath(vm_config_json), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    cli_tests._assert_vm_properties(offer_listing, json_config, 1)
    cli_tests._assert_vm_offer_listing(offer_listing, json_config)
    cli_tests._assert_vm_preview_audience(offer_listing, json_config)
    cli_tests._assert_vm_plan_listing(offer_listing, json_config)


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
