#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest

from swagger_client.rest import ApiException
from tests.cli_groups_tests import (
    st_list_command,
    st_create_command,
    st_show_command,
    st_update_command,
    st_create_plan_command,
    st_list_plan_command,
    st_show_plan_command,
    st_update_plan_command,
)


@pytest.mark.integration
def test_st_list(config_yml, monkeypatch):
    st_list_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_st_create(config_yml, json_listing_config, monkeypatch):
    try:
        st_show_command(config_yml, monkeypatch)

        print("Solution Template Found")
        with pytest.raises(ApiException):
            st_create_command(config_yml, json_listing_config, monkeypatch)
    except:
        st_create_command(config_yml, json_listing_config, monkeypatch)


@pytest.mark.integration
def test_st_update(config_yml, json_listing_config, monkeypatch):
    st_update_command(config_yml, json_listing_config, monkeypatch)


@pytest.mark.integration
def test_st_show(config_yml, monkeypatch):
    st_show_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_st_plan_create(config_yml, json_listing_config, monkeypatch):
    try:
        st_show_plan_command(config_yml, monkeypatch)

        with pytest.raises(ApiException):
            st_create_plan_command(config_yml, json_listing_config, monkeypatch)
    except:
        st_create_plan_command(config_yml, json_listing_config, monkeypatch)


@pytest.mark.integration
def test_st_plan_show(config_yml, monkeypatch):
    st_show_plan_command(config_yml, monkeypatch)


@pytest.mark.integration
def test_st_plan_update(config_yml, json_listing_config, monkeypatch):
    st_update_plan_command(config_yml, json_listing_config, monkeypatch)


@pytest.mark.integration
def test_st_plan_list(config_yml, monkeypatch):
    st_list_plan_command(config_yml, monkeypatch)


# @pytest.mark.integration
# def test_st_publish(config_yml, monkeypatch):
#     st_publish_command(config_yml, monkeypatch)


# @pytest.mark.integration
# def test_st_delete(config_yml, monkeypatch):
#     st_delete_command(config_yml, monkeypatch)
