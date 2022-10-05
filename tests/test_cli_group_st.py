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
    _show_plan_args,
)


@pytest.mark.integration
def test_st_list(config_yml, monkeypatch, capsys):
    st_list_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_st_create(config_yml, json_listing_config, monkeypatch, capsys):
    try:
        st_show_command(config_yml, monkeypatch, capsys)

        print("Solution Template Found")
        with pytest.raises(ApiException):
            st_create_command(config_yml, json_listing_config, monkeypatch, capsys)
    except:
        st_create_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_update(config_yml, json_listing_config, monkeypatch, capsys):
    st_update_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_show(config_yml, monkeypatch, capsys):
    st_show_command(config_yml, monkeypatch, capsys)


@pytest.mark.integration
def test_st_plan_create(config_yml, json_listing_config, monkeypatch, capsys):
    try:
        st_show_plan_command(config_yml, monkeypatch, capsys)

        with pytest.raises(ApiException):
            st_create_plan_command(config_yml, json_listing_config, monkeypatch, capsys)
    except:
        st_create_plan_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_plan_show(config_yml, monkeypatch, capsys):
    output = st_show_plan_command(config_yml, monkeypatch, capsys)
    name = _show_plan_args(config_yml, "st")["plan_name"]
    assert f'"externalID": "{name}",' in output, f"{name} not found in output"


@pytest.mark.integration
def test_st_plan_update(config_yml, json_listing_config, monkeypatch, capsys):
    st_update_plan_command(config_yml, json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_plan_list(config_yml, monkeypatch, capsys):
    st_list_plan_command(config_yml, monkeypatch, capsys)


# @pytest.mark.integration
# def test_st_publish(config_yml, monkeypatch, capsys):
#     st_publish_command(config_yml, monkeypatch, capsys)


# @pytest.mark.integration
# def test_st_release(config_yml, monkeypatch, capsys):
#     st_release_command(config_yml, monkeypatch, capsys)


# @pytest.mark.integration
# def test_st_delete(config_yml, monkeypatch, capsys):
#     st_delete_command(config_yml, monkeypatch, capsys)
