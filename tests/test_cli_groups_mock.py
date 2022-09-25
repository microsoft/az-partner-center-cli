#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest
import json
from pathlib import Path
from adal import AuthenticationContext, adal_error

from tests import cli_groups_tests as cli_tests
from swagger_client import ProductApi

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


def test_vm_list_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.vm_list_command(config_yml, monkeypatch, capsys)


def test_vm_create_success_mock(config_yml, vm_config_json, monkeypatch, capsys):
    vm_config_json = "vm_config.json"
    app_path_fix = "tests/sample_app"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers/test-vm?api-version=2017-10-31"

    # Mock VM offer show API endpoint
    # Set up Requests mock class
    class ShowMockResponse:
        @staticmethod
        def to_dict():
            with open(Path("tests/test_data/vm_show_offer_not_found_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_show_product(self, authorization, **kwargs):
        return ShowMockResponse()

    monkeypatch.setattr(ProductApi, "products_get", mock_show_product)

    # Mock creation VM offer API endpoint
    # Set up Requests mock class
    class CreateMockResponse:
        def __init__(self):
            self.status_code = 200

        @staticmethod
        def json():
            with open(Path("tests/test_data/vm_create_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_create_offer(self, headers, json={}, url=mock_url):
        return CreateMockResponse()

    monkeypatch.setattr(requests, "put", mock_create_offer)
    offer_response = cli_tests.vm_create_command(config_yml, vm_config_json, monkeypatch, capsys)

    offer = json.loads(offer_response)
    with open(Path(app_path_fix).joinpath(vm_config_json), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    cli_tests._assert_vm_properties(offer, json_config)
    cli_tests._assert_vm_offer_listing(offer, json_config)
    cli_tests._assert_vm_preview_audience(offer, json_config)
    cli_tests._assert_vm_plan_listing(offer, json_config)


@pytest.mark.integration
@pytest.mark.xfail(raises=NameError)
def test_vm_create_offer_exists_mock(config_yml, monkeypatch, vm_config_json, capsys):
    vm_config_json = "vm_config.json"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    # Mock VM offer show API endpoint
    # Set up Requests mock class
    class ShowMockResponse:
        @staticmethod
        def to_dict():
            with open(Path("tests/test_data/vm_show_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_show_product(self, authorization, **kwargs):
        return ShowMockResponse()

    monkeypatch.setattr(ProductApi, "products_get", mock_show_product)
    # The create PUT method does not need mocking as the test should fail before that point
    cli_tests.vm_create_command(config_yml, vm_config_json, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=ConnectionError)
def test_vm_create_invalid_offer_mock(config_yml, monkeypatch, capsys):
    # Invalid configuration that creates an offer in a publisher
    # that the user does not have access to
    vm_config_json = "vm_config_unauth_publisher.json"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers/test-vm?api-version=2017-10-31"

    # Mock VM offer show API endpoint
    # Set up Requests mock class
    class ShowMockResponse:
        @staticmethod
        def to_dict():
            with open(Path("tests/test_data/vm_show_offer_not_found_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_show_product(self, authorization, **kwargs):
        return ShowMockResponse()

    monkeypatch.setattr(ProductApi, "products_get", mock_show_product)

    # Expecting a failure as the offer is unable to be created
    cli_tests.vm_create_command(config_yml, vm_config_json, monkeypatch, capsys)


def test_vm_update_mock(config_yml, vm_config_json, monkeypatch, ama_mock, capsys):
    cli_tests.vm_update_command(config_yml, vm_config_json, monkeypatch, capsys)


def test_vm_show_success_mock(config_yml, vm_config_json, monkeypatch, capsys):
    vm_config_json = "vm_config.json"
    app_path_fix = "tests/sample_app"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    # Mock VM offer show API endpoint
    # Set up Requests mock class
    class ShowMockResponse:
        @staticmethod
        def to_dict():
            with open(Path("tests/test_data/vm_show_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_show_product(self, authorization, **kwargs):
        return ShowMockResponse()

    monkeypatch.setattr(ProductApi, "products_get", mock_show_product)

    offer_response = cli_tests.vm_show_command(config_yml, vm_config_json, monkeypatch, capsys)

    # Load mocked API JSON response
    offer_listing = json.loads(offer_response)

    # Load JSON config file for assertions
    with open(Path(app_path_fix).joinpath(vm_config_json), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    cli_tests._assert_vm_show(offer_listing, json_config)


@pytest.mark.integration
@pytest.mark.xfail(raises=adal_error.AdalError)
def test_vm_show_invalid_auth_details_mock(config_yml, monkeypatch, capsys):
    # Invalid config yaml file using incorrect client ID & secret
    config_yml = "tests/sample_app/config_invalid.yml"

    # Valid JSON configuration file
    json_listing_config = "vm_config.json"

    # Mock authorization token retreival to return an error
    def mock_get_auth(self, resource, client_id, client_secret):
        raise adal_error.AdalError(
            'Get Token request returned http error: 401 and server response: {"error":"invalid_client","error_description":"AADSTS7000215: Invalid client secret provided. Ensure the secret being sent in the request is the client secret value, not the client secret ID, for a secret added to app'
        )

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    cli_tests.vm_show_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=LookupError)
def test_vm_show_invalid_offer_mock(config_yml, monkeypatch, capsys):
    # Invalid configuration to show an offer that doesnt exist
    vm_config_json = "vm_config_uncreated_offer.json"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers/test-vm?api-version=2017-10-31"

    # Mock VM offer show API endpoint
    # Set up Requests mock class
    class ShowMockResponse:
        @staticmethod
        def to_dict():
            with open(Path("tests/test_data/vm_show_offer_not_found_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_show_product(self, authorization, **kwargs):
        return ShowMockResponse()

    monkeypatch.setattr(ProductApi, "products_get", mock_show_product)

    # Expecting a failure as the offer does not exist
    cli_tests.vm_show_command(config_yml, vm_config_json, monkeypatch, capsys)


def test_vm_list_success_mock(config_yml, vm_config_json, monkeypatch, capsys):
    """only must return the VM offers"""
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
            with open(Path("tests/test_data/vm_list_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers?api-version=2017-10-31&$filter=offerTypeId"

    def mock_list_offer(self, headers, url=mock_url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_list_offer)

    response = cli_tests.vm_list_command(config_yml, monkeypatch, capsys)

    # Load mocked API JSON response
    vm_list = json.loads(response)

    # Load JSON config file for assertions
    with open(Path(app_path_fix).joinpath(vm_config_json), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    cli_tests._assert_vm_list_all_offers(vm_list, json_config)


def test_vm_list_empty_success_mock(config_yml, vm_config_json, monkeypatch, capsys):
    """only must return the VM offers"""
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
            with open(Path("tests/test_data/vm_list_empty_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers?api-version=2017-10-31&$filter=offerTypeId"

    def mock_list_offer(self, headers, url=mock_url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_list_offer)

    response = cli_tests.vm_list_command(config_yml, monkeypatch, capsys)

    # Load mocked API JSON response
    vm_list = json.loads(response)

    cli_tests._assert_vm_empty_listing(vm_list)


@pytest.mark.integration
@pytest.mark.xfail(raises=ValueError)
def test_vm_list_missing_publisher_id_mock(config_yml, monkeypatch, capsys):
    # No mocks required because it does not hit any APIs
    cli_tests.vm_list_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=adal_error.AdalError)
def test_vm_list_invalid_auth_details_mock(config_yml, monkeypatch, capsys):
    # Invalid config yaml file using incorrect client ID & secret
    config_yml = "tests/sample_app/config_invalid.yml"

    # Mock authorization token retreival to return an error
    def mock_get_auth(self, resource, client_id, client_secret):
        raise adal_error.AdalError(
            'Get Token request returned http error: 401 and server response: {"error":"invalid_client","error_description":"AADSTS7000215: Invalid client secret provided. Ensure the secret being sent in the request is the client secret value, not the client secret ID, for a secret added to app'
        )

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    cli_tests.vm_list_command(config_yml, monkeypatch, capsys)


def test_vm_publish_success_mock(config_yml, monkeypatch, capsys):
    vm_config_json = "vm_config.json"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    # Mock VM offer publish API endpoint
    # Set up Requests mock class
    class MockResponse:
        def __init__(self):
            self.status_code = 202

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers/test-vm/publish?api-version=2017-10-31"

    def mock_publish_offer(self, headers, url=mock_url, json={}):
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_publish_offer)

    response = cli_tests.vm_publish_command(config_yml, vm_config_json, monkeypatch, capsys)

    assert json.loads(response) == True


@pytest.mark.integration
@pytest.mark.xfail(raises=ValueError)
def test_vm_publish_missing_publisher_id_mock(config_yml, monkeypatch, capsys):
    # Invalid JSON config with missing publisher ID
    vm_config_json = "vm_config_missing_publisher_id.json"

    # No mocks required because it does not hit any APIs
    cli_tests.vm_publish_command(config_yml, vm_config_json, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=adal_error.AdalError)
def test_vm_publish_invalid_auth_details_mock(config_yml, monkeypatch, capsys):
    # Invalid config yaml file using incorrect client ID & secret
    config_yml = "tests/sample_app/config_invalid.yml"

    # Valid JSON configuration file
    json_listing_config = "vm_config.json"

    # Mock authorization token retreival to return an error
    def mock_get_auth(self, resource, client_id, client_secret):
        raise adal_error.AdalError("Get Token request returned http error: 401 and server response: ...")

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    cli_tests.vm_publish_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=ConnectionError)
def test_vm_publish_offer_does_not_exist_mock(config_yml, monkeypatch, capsys):
    # Invalid configuration to show an offer that doesnt exist
    vm_config_json = "vm_config_uncreated_offer.json"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers/test-vm/publish?api-version=2017-10-31"

    # Mock the show VM offer API method
    class ShowMockResponse:
        def __init__(self):
            self.status_code = 404
            self.text = "Mock Response"

        @staticmethod
        def json():
            return "Microsoft.Ingestion.Api.Common.Exceptions.Http404Exception..."

    def mock_publish_offer(self, headers, url=mock_url, json={}):
        return ShowMockResponse()

    monkeypatch.setattr(requests, "post", mock_publish_offer)

    # Expecting a failure as the offer does not exist
    cli_tests.vm_publish_command(config_yml, vm_config_json, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=ConnectionError)
def test_vm_publish_invalid_offer_mock(config_yml, monkeypatch, capsys):
    # Invalid configuration to show an offer that doesnt exist
    vm_config_json = "vm_config.json"

    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    mock_url = "https://cloudpartner.azure.com/api/publishers/contoso/offers/test-vm/publish?api-version=2017-10-31"

    # Mock the show VM offer API method
    class ShowMockResponse:
        def __init__(self):
            self.status_code = 422
            self.text = "Mock Response"

        @staticmethod
        def json():
            return "Microsoft.Ingestion.Api.Common.Exceptions.Http422Exception..."

    def mock_publish_offer(self, headers, url=mock_url, json={}):
        return ShowMockResponse()

    monkeypatch.setattr(requests, "post", mock_publish_offer)

    # Expecting a failure as the offer does not exist
    cli_tests.vm_publish_command(config_yml, vm_config_json, monkeypatch, capsys)


def test_vm_delete_success_mock(config_yml, monkeypatch, capsys):
    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    # Mock VM offer show API endpoint
    # Set up Requests mock class
    class ShowMockResponse:
        @staticmethod
        def to_dict():
            with open(Path("tests/test_data/vm_show_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_show_product(self, authorization, **kwargs):
        return ShowMockResponse()

    monkeypatch.setattr(ProductApi, "products_get", mock_show_product)

    # Mock VM offer delete API endpoint
    def mock_delete_product(self, product_id, authorization, **kwargs):
        return ""

    monkeypatch.setattr(ProductApi, "products_product_id_delete", mock_delete_product)
    cli_tests.vm_delete_command(config_yml, monkeypatch, capsys)


@pytest.mark.xfail(raises=LookupError)
def test_vm_delete_offer_doesnot_exist_mock(config_yml, monkeypatch, capsys):
    # Mock authorization token retreival
    def mock_get_auth(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    # Mock VM offer show API endpoint
    # Set up Requests mock class
    class ShowMockResponse:
        @staticmethod
        def to_dict():
            with open(Path("tests/test_data/vm_show_offer_not_found_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_show_product(self, authorization, **kwargs):
        return ShowMockResponse()

    monkeypatch.setattr(ProductApi, "products_get", mock_show_product)

    cli_tests.vm_delete_command(config_yml, monkeypatch, capsys)


@pytest.mark.xfail(raises=adal_error.AdalError)
def test_vm_delete_invalid_auth_details_mock(config_yml, monkeypatch, capsys):
    # Invalid config yaml file using incorrect client ID & secret
    config_yml = "tests/sample_app/config_invalid.yml"

    # Mock authorization token retreival to return an error
    def mock_get_auth(self, resource, client_id, client_secret):
        raise adal_error.AdalError("Get Token request returned http error: 401 and server response: ...")

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", mock_get_auth)

    cli_tests.vm_delete_command(config_yml, monkeypatch, capsys)


def test_ma_list_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.ma_list_command(config_yml, monkeypatch, capsys)


def test_ma_create_mock(config_yml, ma_config_json, monkeypatch, ama_mock, capsys):
    cli_tests.ma_create_command(config_yml, ma_config_json, monkeypatch, capsys)


def test_ma_update_mock(config_yml, ma_config_json, monkeypatch, ama_mock, capsys):
    cli_tests.ma_update_command(config_yml, ma_config_json, monkeypatch, capsys)


def test_ma_show_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.ma_show_command(config_yml, monkeypatch, capsys)


def test_ma_publish_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.ma_publish_command(config_yml, monkeypatch, capsys)


def test_ma_release_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.ma_release_command(config_yml, monkeypatch, capsys)


def test_ma_delete_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.ma_delete_command(config_yml, monkeypatch, capsys)


def test_st_list_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.st_list_command(config_yml, monkeypatch, capsys)


def test_st_create_mock(config_yml, st_config_json, monkeypatch, ama_mock, capsys):
    cli_tests.st_create_command(config_yml, st_config_json, monkeypatch, capsys)


def test_st_update_mock(config_yml, st_config_json, monkeypatch, ama_mock, capsys):
    cli_tests.st_update_command(config_yml, st_config_json, monkeypatch, capsys)


def test_st_show_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.st_show_command(config_yml, monkeypatch, capsys)


def test_st_publish_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.st_publish_command(config_yml, monkeypatch, capsys)


def test_st_release_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.st_release_command(config_yml, monkeypatch, capsys)


def test_st_delete_mock(config_yml, monkeypatch, ama_mock, capsys):
    cli_tests.st_delete_command(config_yml, monkeypatch, capsys)
