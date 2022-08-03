#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import json
from pathlib import Path

import pytest
from swagger_client.rest import ApiException

from azureiai.partner_center.offers.container import Container

from tests.cli_groups_tests import (
    co_list_command,
    _assert_properties,
    _assert_offer_listing,
    _assert_preview_audience,
    co_update_command,
    co_show_command,
    co_create_command,
    co_create_plan_command,
    co_show_plan_command,
    co_update_plan_command,
    co_list_plan_command,
    co_delete_plan_command,
    co_publish_command,
    co_delete_command,
)


@pytest.mark.integration
def test_co_list(config_yml, monkeypatch, capsys):
    co_list_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_co_create(config_yml, monkeypatch, app_path_fix, json_listing_config, capsys):
    try:
        co_show_command(config_yml, monkeypatch, capsys)

        print("Managed App Found")
        with pytest.raises(ApiException):
            co_create_command(config_yml, json_listing_config, monkeypatch, capsys)
    except:
        co_create_command(config_yml, json_listing_config, monkeypatch, capsys)

    offer = Container(name="test_co")
    offer.show()
    with open(Path(app_path_fix).joinpath(json_listing_config), "r", encoding="utf8") as read_file:
        json_config = json.load(read_file)

    _assert_properties(offer, json_config)
    _assert_offer_listing(offer, json_config)
    # _assert_preview_audience(offer, json_config) # todo: Preview Audience not working for Containers


@pytest.mark.integration
def test_co_update(config_yml, json_listing_config, monkeypatch, capsys):
    co_update_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_co_show(config_yml, monkeypatch, capsys):
    co_show_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_co_plan_create(config_yml, json_listing_config, monkeypatch, capsys):
    co_create_plan_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_co_plan_show(config_yml, monkeypatch, capsys):
    co_show_plan_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_co_plan_update(config_yml, json_listing_config, monkeypatch, capsys):
    co_update_plan_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_co_plan_list(config_yml, monkeypatch, capsys):
    co_list_plan_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_co_plan_delete(config_yml, monkeypatch, capsys):
    co_delete_plan_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_co_publish(config_yml, monkeypatch, capsys):
    co_publish_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_co_delete(config_yml, monkeypatch, capsys):
    co_delete_command(config_yml, monkeypatch, capsys)
