#  ---------------------------------------------------------
#  Copyright (c) 2020 Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest

from swagger_client.rest import ApiException
from tests.cli_groups_tests import (
    _show_plan_args,
    st_create_command,
    st_create_plan_command,
    st_delete_command,
    st_list_command,
    st_list_plan_command,
    st_publish_command,
    st_release_command,
    st_show_command,
    st_show_plan_command,
    st_update_command,
    st_update_plan_command,
)


@pytest.mark.integration
def test_st_list(monkeypatch, capsys):
    st_list_command(monkeypatch, capsys)


@pytest.mark.integration
def test_st_create(json_listing_config, monkeypatch, capsys):
    try:
        st_show_command(monkeypatch, capsys)

        print("Solution Template Found")
        with pytest.raises(ApiException):
            st_create_command(json_listing_config, monkeypatch, capsys)
    except:
        st_create_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_update(json_listing_config, monkeypatch, capsys):
    st_update_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_show(monkeypatch, capsys):
    st_show_command(monkeypatch, capsys)


@pytest.mark.integration
def test_st_plan_create(json_listing_config, monkeypatch, capsys):
    try:
        st_show_plan_command(monkeypatch, capsys)

        with pytest.raises(ApiException):
            st_create_plan_command(json_listing_config, monkeypatch, capsys)
    except:
        st_create_plan_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_plan_show(monkeypatch, capsys):
    output = st_show_plan_command(monkeypatch, capsys)
    name = _show_plan_args("st")["plan_name"]
    assert f'"externalID": "{name}",' in output, f"{name} not found in output"


@pytest.mark.integration
def test_st_plan_update(json_listing_config, monkeypatch, capsys):
    st_update_plan_command(json_listing_config, monkeypatch, capsys)


@pytest.mark.integration
def test_st_plan_list(monkeypatch, capsys):
    st_list_plan_command(monkeypatch, capsys)


@pytest.mark.skip
def test_st_publish(monkeypatch, capsys):
    st_publish_command(monkeypatch, capsys)


@pytest.mark.skip
def test_st_release(monkeypatch, capsys):
    st_release_command(monkeypatch, capsys)


@pytest.mark.integration
def test_st_delete(monkeypatch, capsys):
    st_delete_command(monkeypatch, capsys)
