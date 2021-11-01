#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import json
from pathlib import Path

import pytest

from azureiai.partner_center import Plan
from azureiai.partner_center.offers.virtual_machine import VirtualMachine
from swagger_client.rest import ApiException
from tests.cli_groups_tests import (
    vm_list_command,
    vm_create_command,
    vm_show_command,
    vm_update_command,
    vm_delete_command,
    vm_list_plan_command,
    vm_create_plan_command,
    vm_show_plan_command,
    vm_update_plan_command,
    vm_delete_plan_command, _assert_properties, _assert_offer_listing, _assert_plan_listing,
    _assert_pricing_and_availability, _assert_technical_configuration,
)


@pytest.mark.integration
def test_vm_list(config_yml, monkeypatch):
    vm_list_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_create(config_yml, monkeypatch, app_path_fix, json_listing_config):
    try:
        vm_show_command(config_yml, monkeypatch)

        print("Managed App Found")
        with pytest.raises(ApiException):
            vm_create_command(config_yml, monkeypatch)
    except:
        vm_create_command(config_yml, monkeypatch)

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
def test_vm_update(config_yml, monkeypatch):
    vm_update_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_vm_plan_create(config_yml, monkeypatch, app_path_fix, json_listing_config):
    try:
        vm_show_plan_command(config_yml, monkeypatch)

        with pytest.raises(ApiException):
            vm_create_plan_command(config_yml, monkeypatch)
    except:
        vm_create_plan_command(config_yml, monkeypatch)

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
    vm_update_plan_command(config_yml, monkeypatch)

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

# @pytest.mark.integration
# def test_vm_publish(config_yml, monkeypatch):
#     vm_publish_command(config_yml, monkeypatch)
