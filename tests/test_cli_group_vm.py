#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import json
import os
from pathlib import Path

import pytest
import requests
from adal import AuthenticationContext

from azure.partner_center.plan import Plan
from swagger_client.rest import ApiException
from tests.cli_groups_tests import (_assert_plan_listing, _assert_pricing_and_availability,
                                    _assert_technical_configuration, _assert_vm_offer_listing,
                                    _assert_vm_offer_listing_integration, _assert_vm_plan_listing,
                                    _assert_vm_preview_audience, _assert_vm_properties, _assert_vm_show,
                                    vm_create_command, vm_create_plan_command, vm_delete_command,
                                    vm_delete_plan_command, vm_list_command, vm_list_plan_command, vm_publish_command,
                                    vm_show_command, vm_show_plan_command, vm_update_plan_command)


@pytest.fixture()
def vm_offer_setup(monkeypatch, capsys):
    json_listing_config = "vm_config.json"
    vm_create_command(json_listing_config, monkeypatch, capsys)
    yield


@pytest.fixture()
def vm_offer_teardown(monkeypatch, capsys):
    yield
    vm_delete_command(monkeypatch, capsys)


@pytest.fixture()
def vm_offer_setup_teardown(vm_offer_setup, vm_offer_teardown):
    return


@pytest.mark.integration
def test_vm_get(monkeypatch, app_path_fix):
    with open(Path(app_path_fix).joinpath("vm_listing_config.json"), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

        publisher_id = json_config["publisherId"]
        offer_id = json_config["id"]

        url = f"https://cloudpartner.azure.com/api/publishers/{publisher_id}/offers/{offer_id}?api-version=2017-10-31"
        headers = {"Authorization": "Bearer " + management_access_key(), "Content-Type": "application/json"}

        response = requests.get(url, headers=headers)
        assert response.status_code == 200, json.dumps(response.json(), indent=4)
        print(json.dumps(response.json(), indent=4))


@pytest.mark.integration
def test_vm_update(monkeypatch, app_path_fix):
    with open(Path(app_path_fix).joinpath("vm_listing_config.json"), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)
        json_config["publisherId"] = "microsoftcorporation1590077852919"

        json_config["definition"]["plans"][0]["microsoft-azure-virtualmachines.vmImages"]["0.0.0"][
            "osVhdUrl"
        ] = os.getenv("win10UnrealVHD")
        json_config["definition"]["plans"][1]["microsoft-azure-virtualmachines.vmImages"]["0.0.0"][
            "osVhdUrl"
        ] = os.getenv("win10UnityVHD")
        json_config["definition"]["plans"][2]["microsoft-azure-virtualmachines.vmImages"]["0.0.0"][
            "osVhdUrl"
        ] = os.getenv("ws2019UnrealVHD")
        json_config["definition"]["plans"][3]["microsoft-azure-virtualmachines.vmImages"]["0.0.0"][
            "osVhdUrl"
        ] = os.getenv("ws2019UnityVHD")

        json_config["definition"]["offer"]["microsoft-azure-marketplace.smallLogo"] = os.getenv("smallLogo")
        json_config["definition"]["offer"]["microsoft-azure-marketplace.mediumLogo"] = os.getenv("mediumLogo")
        json_config["definition"]["offer"]["microsoft-azure-marketplace.largeLogo"] = os.getenv("largeLogo")
        json_config["definition"]["offer"]["microsoft-azure-marketplace.wideLogo"] = os.getenv("wideLogo")
        json_config["definition"]["offer"]["microsoft-azure-marketplace.heroLogo"] = os.getenv("heroLogo")

        print(json.dumps(json_config, indent=4))
        publisher_id = json_config["publisherId"]
        offer_id = json_config["id"]

        url = f"https://cloudpartner.azure.com/api/publishers/{publisher_id}/offers/{offer_id}?api-version=2017-10-31"
        headers = {"Authorization": "Bearer " + management_access_key(), "Content-Type": "application/json"}

        response = requests.put(url, json=json_config, headers=headers)
        assert response.status_code == 200, json.dumps(response.json(), indent=4)


def management_access_key():
    """Create a Auth Client for interacting with CCP"""

    auth_context = AuthenticationContext("https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47")
    token_response = auth_context.acquire_token_with_client_credentials(
        resource="https://cloudpartner.azure.com",
        client_id=credential()["aad_id"],
        client_secret=credential()["aad_secret"],
    )
    return token_response["accessToken"]


def _get_access_key(resource):
    tenant_id = credential()["tenant_id"]
    aad_id = credential()["aad_id"]
    secret = credential()["aad_secret"]

    url = "https://login.microsoftonline.com/%s/oauth2/token" % tenant_id
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials", "client_id": aad_id, "client_secret": secret, "resource": resource}

    response = requests.post(url=url, data=data, headers=headers)
    if response.status_code != 200:
        raise ConnectionRefusedError("Unable to create Azure Active Directory access token")
    return response.json()["access_token"]


def credential():
    """
    Load Credentials from environment Azure Account

    Returns: dict of information used for authentication to Azure

    """
    return {
        "aad_id": os.getenv("AAD_ID"),
        "object_id": os.getenv("OBJ_ID"),
        "aad_secret": os.getenv("AAD_SECRET"),
        "tenant_id": os.getenv("TENANT_ID"),
        "azure_preview_subscription": os.getenv("SUBSCRIPTION_ID"),
    }


@pytest.mark.integration
def test_vm_list(monkeypatch, capsys):
    vm_list_command(monkeypatch, capsys)


@pytest.mark.integration
def test_vm_create_success(monkeypatch, app_path_fix, json_listing_config, vm_offer_teardown, capsys):
    json_listing_config = "vm_config.json"
    app_path_fix = "tests/sample_app"

    offer_response = vm_create_command(json_listing_config, monkeypatch, capsys)

    if offer_response:
        offer = json.loads(offer_response)
        with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
            json_config = json.load(read_file)

        _assert_vm_properties(offer, json_config)
        _assert_vm_offer_listing(offer, json_config)
        _assert_vm_preview_audience(offer, json_config)
        _assert_vm_plan_listing(offer, json_config)


@pytest.mark.integration
@pytest.mark.xfail(raises=NameError)
def test_vm_create_offer_exists(monkeypatch, app_path_fix, json_listing_config, capsys):
    json_listing_config = "vm_config.json"
    app_path_fix = "tests/sample_app"

    # Create offer first time
    vm_create_command(json_listing_config, monkeypatch, capsys)

    # Create the same offer as second time
    vm_create_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=ConnectionError)
def test_vm_create_invalid_offer(monkeypatch, capsys):
    # Invalid configuration that creates an offer in a publisher
    # that the user does not have access to
    json_listing_config = "vm_config_unauth_publisher.json"

    # Expecting a failure as the offer is unable to be created
    vm_create_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_vm_show_success(vm_offer_setup_teardown, monkeypatch, capsys):
    json_listing_config = "vm_config.json"
    app_path_fix = "tests/sample_app"

    offer_response = vm_show_command(json_listing_config, monkeypatch, capsys)

    # Load API JSON response
    offer_listing = json.loads(offer_response)

    # Load JSON config file for assertions
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_vm_show(offer_listing, json_config)


@pytest.mark.integration
@pytest.mark.xfail(raises=LookupError)
def test_vm_show_invalid_offer(monkeypatch, capsys):
    # Invalid configuration to show an offer that doesnt exist
    json_listing_config = "vm_config_uncreated_offer.json"

    # Expecting a failure as the offer does not exist
    vm_show_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_vm_list_success(vm_offer_setup_teardown, monkeypatch, capsys):
    offer_response = vm_list_command(monkeypatch, capsys)

    # Load API JSON response
    vm_offer_listing = json.loads(offer_response)
    _assert_vm_offer_listing_integration(vm_offer_listing)


@pytest.mark.integration
@pytest.mark.xfail(raises=ValueError)
def test_vm_list_missing_publisher_id(monkeypatch, capsys):
    # Expecting a Value error when unable to access Publisher ID
    vm_list_command(monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.skip(reason="Need to determine how to clean up test safely")
def test_vm_publish_success(vm_offer_setup_teardown, monkeypatch, capsys):
    # Need to determine how to clean up tests so that it cancels the publish
    # operation and can then delete the offer
    json_listing_config = "vm_config.json"

    offer_response = vm_publish_command(json_listing_config, monkeypatch, capsys)

    print(offer_response)


@pytest.mark.integration
@pytest.mark.xfail(raises=ValueError)
def test_vm_publish_missing_publisher_id(monkeypatch, capsys):
    # Invalid JSON config with missing publisher ID
    json_listing_config = "vm_config_missing_publisher_id.json"

    # Expecting a Value error when unable to access Publisher ID
    vm_publish_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=ConnectionError)
def test_vm_publish_offer_doesnot_exist(monkeypatch, capsys):
    # Invalid configuration to show an offer that doesnt exist
    json_listing_config = "vm_config_uncreated_offer.json"

    # Confirm that the offer does not exist
    with pytest.raises(LookupError):
        vm_show_command(json_listing_config, monkeypatch, capsys)

    # Expecting a failure as the offer does not exist
    vm_publish_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=ConnectionError)
def test_vm_publish_invalid_offer(monkeypatch, capsys):
    # All of the required config is not set, so unable to publish offer
    json_listing_config = "vm_invalid_config.json"

    # Expecting a failure as the offer isnt fully configured
    vm_publish_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_vm_delete_success(vm_offer_setup, monkeypatch, capsys):
    json_listing_config = "vm_config.json"

    vm_delete_command(monkeypatch)

    # Confirm that the offer has been deleted
    with pytest.raises(LookupError):
        vm_show_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
@pytest.mark.xfail(raises=LookupError)
def test_vm_delete_offer_doesnot_exist(monkeypatch, capsys):
    vm_delete_command(monkeypatch, capsys)


@pytest.mark.integration
def test_vm_plan_create(monkeypatch, app_path_fix, json_listing_config, capsys):
    try:
        vm_show_plan_command(monkeypatch, capsys)

        with pytest.raises(ApiException):
            vm_create_plan_command(json_listing_config, monkeypatch, capsys)
    except:
        vm_create_plan_command(json_listing_config, monkeypatch, capsys)

    offer = Plan(name="test_vm", plan_name="test_vm_plan")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_plan_listing(offer, json_config)
    _assert_pricing_and_availability(offer, json_config)
    _assert_technical_configuration(offer, json_config)


@pytest.mark.integration
def test_vm_plan_show(monkeypatch, capsys):
    vm_show_plan_command(monkeypatch, capsys)


@pytest.mark.integration
def test_vm_plan_update(monkeypatch, app_path_fix, json_listing_config, capsys):
    vm_update_plan_command(json_listing_config, monkeypatch, capsys)

    offer = Plan(name="test_vm", plan_name="test_vm_plan")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_plan_listing(offer, json_config)
    _assert_pricing_and_availability(offer, json_config)
    _assert_technical_configuration(offer, json_config)


@pytest.mark.integration
def test_vm_plan_list(monkeypatch, capsys):
    vm_list_plan_command(monkeypatch, capsys)


@pytest.mark.integration
def test_vm_plan_delete(monkeypatch, capsys):
    vm_delete_plan_command(monkeypatch, capsys)
