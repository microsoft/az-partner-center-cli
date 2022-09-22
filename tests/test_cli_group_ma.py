#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import json
from pathlib import Path

import pytest

from azureiai.partner_center.plan import Plan
from azureiai.partner_center.offers.managed_app import ManagedApp

from swagger_client.rest import ApiException
from tests.cli_groups_tests import (
    ma_list_command,
    ma_create_command,
    ma_show_command,
    ma_update_command,
    ma_delete_command,
    ma_publish_command,
    ma_list_plan_command,
    ma_create_plan_command,
    ma_show_plan_command,
    ma_update_plan_command,
    ma_delete_plan_command,
    _assert_properties,
    _assert_offer_listing,
    _assert_preview_audience,
    _assert_plan_listing,
    _assert_pricing_and_availability,
    _assert_technical_configuration,
)


@pytest.mark.integration
def test_ma_list(config_yml, monkeypatch, capsys):
    ma_list_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_ma_create(config_yml, monkeypatch, app_path_fix, json_listing_config, capsys):
    try:
        ma_show_command(config_yml, monkeypatch, capsys)

        print("Managed App Found")
        with pytest.raises(ApiException):
            ma_create_command(config_yml, json_listing_config, monkeypatch, capsys)
    except:
        ma_create_command(config_yml, json_listing_config, monkeypatch, capsys)

    # Load Managed App
    offer = ManagedApp(name="test_ma")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_properties(offer, json_config)
    _assert_offer_listing(offer, json_config)
    _assert_preview_audience(offer, json_config)


@pytest.mark.integration
def test_ma_update(config_yml, json_listing_config, monkeypatch, capsys):
    ma_update_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_ma_show(config_yml, monkeypatch, capsys):
    ma_show_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_ma_plan_create(config_yml, monkeypatch, app_path_fix, json_listing_config, capsys):
    ma_create_plan_command(config_yml, json_listing_config, monkeypatch, capsys)

    offer = Plan(name="test_ma", plan_name="test_ma_plan")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_plan_listing(offer, json_config)
    _assert_pricing_and_availability(offer, json_config)
    _assert_technical_configuration(offer, json_config)


@pytest.mark.integration
def test_ma_plan_show(config_yml, monkeypatch, capsys):
    ma_show_plan_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_ma_plan_update(config_yml, monkeypatch, app_path_fix, json_listing_config, capsys):
    ma_update_plan_command(config_yml, json_listing_config, monkeypatch, capsys)

    offer = Plan(name="test_ma", plan_name="test_ma_plan")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_plan_listing(offer, json_config)
    _assert_pricing_and_availability(offer, json_config)
    _assert_technical_configuration(offer, json_config)


@pytest.mark.integration
def test_ma_plan_list(config_yml, monkeypatch, capsys):
    ma_list_plan_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_ma_plan_delete(config_yml, monkeypatch, capsys):
    ma_delete_plan_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_ma_publish(config_yml, monkeypatch, capsys):
    ma_publish_command(config_yml, monkeypatch, capsys)


# @pytest.mark.integration
# def test_ma_release(config_yml, monkeypatch, capsys):
#     ma_release_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_ma_delete(config_yml, monkeypatch, capsys):
    ma_delete_command(config_yml, monkeypatch, capsys)
