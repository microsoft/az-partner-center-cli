#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import json
import os
from pathlib import Path

import pytest
import requests
from adal import AuthenticationContext

from azureiai.partner_center.offers.virtual_machine import VirtualMachine
from azureiai.partner_center.plan import Plan
from swagger_client.rest import ApiException
from tests.cli_groups_tests import (
    vm_list_command,
    vm_create_command,
    vm_show_command,
    vm_delete_command,
    vm_list_plan_command,
    vm_create_plan_command,
    vm_show_plan_command,
    vm_update_plan_command,
    vm_delete_plan_command,
    _assert_properties,
    _assert_offer_listing,
    _assert_plan_listing,
    _assert_pricing_and_availability,
    _assert_technical_configuration,
)


@pytest.mark.integration
def test_vm_get(config_yml, monkeypatch, app_path_fix):
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
def test_vm_update(config_yml, monkeypatch, app_path_fix):
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
def test_vm_list(config_yml, monkeypatch):
    vm_list_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_create(config_yml, monkeypatch, app_path_fix, json_listing_config):
    try:
        vm_show_command(config_yml, monkeypatch)

        print("Managed App Found")
        with pytest.raises(ApiException):
            vm_create_command(config_yml, json_listing_config, monkeypatch)
    except:
        vm_create_command(config_yml, json_listing_config, monkeypatch)

    offer = VirtualMachine(name="test_vm")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_properties(offer, json_config)
    _assert_offer_listing(offer, json_config)
    # _assert_preview_audience(offer, json_config)  # todo: Preview Audience for VM not working


@pytest.mark.integration
def test_vm_show(config_yml, monkeypatch):
    vm_show_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_plan_create(config_yml, monkeypatch, app_path_fix, json_listing_config):
    try:
        vm_show_plan_command(config_yml, monkeypatch)

        with pytest.raises(ApiException):
            vm_create_plan_command(config_yml, json_listing_config, monkeypatch)
    except:
        vm_create_plan_command(config_yml, json_listing_config, monkeypatch)

    offer = Plan(name="test_vm", plan_name="test_vm_plan")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_plan_listing(offer, json_config)
    _assert_pricing_and_availability(offer, json_config)
    _assert_technical_configuration(offer, json_config)


@pytest.mark.integration
def test_vm_plan_show(config_yml, monkeypatch):
    vm_show_plan_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_plan_update(config_yml, monkeypatch, app_path_fix, json_listing_config):
    vm_update_plan_command(config_yml, json_listing_config, monkeypatch)

    offer = Plan(name="test_vm", plan_name="test_vm_plan")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_plan_listing(offer, json_config)
    _assert_pricing_and_availability(offer, json_config)
    _assert_technical_configuration(offer, json_config)


@pytest.mark.integration
def test_vm_plan_list(config_yml, monkeypatch):
    vm_list_plan_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_plan_delete(config_yml, monkeypatch):
    vm_delete_plan_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_delete(config_yml, monkeypatch):
    vm_delete_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_publish(config_yml, monkeypatch):
    vm_publish_command(config_yml, monkeypatch)
