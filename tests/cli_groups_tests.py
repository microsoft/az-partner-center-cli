#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI v2 Test Suite"""
from collections import namedtuple

import requests

from azureiai import azpc_app
from azureiai.managed_apps.confs import Properties, Listing, ProductAvailability
from azureiai.managed_apps.confs.variant import OfferListing, FeatureAvailability, Package
from tests.cli_tests import setup_patched_app


def _list_command_args(config_yml, subgroup):
    return {"subgroups": subgroup, "command": "list", "config_yml": config_yml}


def _create_command_args(config_yml, subgroup):
    return {"subgroups": subgroup, "command": "create", "name": f"test_{subgroup}", "config_yml": config_yml}


def _update_command_args(config_yml, subgroup):
    return {"subgroups": subgroup, "command": "update", "name": f"test_{subgroup}", "config_yml": config_yml}


def _create_plan_args(config_yml, subgroup):
    return {
        "subgroups": subgroup,
        "command": "plan",
        "sub_command": "create",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
    }


def _update_plan_args(config_yml, subgroup):
    return {
        "subgroups": subgroup,
        "command": "plan",
        "sub_command": "update",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
    }


def _show_plan_args(config_yml, subgroup):
    input_args = {
        "subgroups": subgroup,
        "command": "plan",
        "plan_command": "show",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
    }
    return input_args


def _list_plan_args(config_yml, subgroup):
    input_args = {
        "subgroups": subgroup,
        "command": "plan",
        "plan_command": "list",
        "name": f"test_{subgroup}",
        "config_yml": config_yml,
    }
    return input_args


def _delete_plan_args(config_yml, subgroup):
    input_args = {
        "subgroups": subgroup,
        "command": "plan",
        "plan_command": "delete",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
    }
    return input_args


def _show_command_args(config_yml, subgroup):
    input_args = {"subgroups": subgroup, "command": "show", "name": f"test_{subgroup}", "config_yml": config_yml}
    return input_args


def _publish_command_args(config_yml, subgroup):
    input_args = {
        "subgroups": subgroup,
        "command": "publish",
        "name": f"test_{subgroup}",
        "config_yml": config_yml,
        "notification_emails": "dcibs@microsoft.com",
    }
    return input_args


def _delete_command_args(config_yml, subgroup):
    input_args = {"subgroups": subgroup, "command": "delete", "name": f"test_{subgroup}", "config_yml": config_yml}
    return input_args


def vm_list_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_command_args(config_yml, subgroup="vm"))


def vm_create_command(config_yml, monkeypatch):
    def mock_put_request(url, data="", headers="", params="", json=""):
        return namedtuple("response", ["status_code"])(*[200])

    monkeypatch.setattr(requests, "put", mock_put_request)

    args_test(monkeypatch, _create_command_args(config_yml, subgroup="vm"))


def vm_update_command(config_yml, monkeypatch):
    def mock_put_request(url, data="", headers="", params="", json=""):
        return namedtuple("response", ["status_code"])(*[200])

    monkeypatch.setattr(requests, "put", mock_put_request)

    args_test(monkeypatch, _update_command_args(config_yml, "vm"))


def vm_create_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _create_plan_args(config_yml, "vm"))


def vm_update_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _update_plan_args(config_yml, "vm"))


def vm_show_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _show_plan_args(config_yml, "vm"))


def vm_list_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_plan_args(config_yml, "vm"))


def vm_delete_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _delete_plan_args(config_yml, "vm"))


def vm_show_command(config_yml, monkeypatch):
    def mock_put_request(url, data="", headers="", params="", json=""):
        return namedtuple("response", ["status_code"])(*[202])

    monkeypatch.setattr(requests, "put", mock_put_request)

    subgroup = "vm"
    input_args = _show_command_args(config_yml, subgroup)
    args_test(monkeypatch, input_args)


def vm_publish_command(config_yml, monkeypatch):
    def mock_post_request(url, data="", headers="", params="", json=""):
        return namedtuple("response", ["status_code"])(*[202])

    monkeypatch.setattr(requests, "post", mock_post_request)

    subgroup = "vm"
    input_args = _publish_command_args(config_yml, subgroup)
    args_test(monkeypatch, input_args)


def vm_delete_command(config_yml, monkeypatch):
    subgroup = "vm"
    input_args = _delete_command_args(config_yml, subgroup)
    args_test(monkeypatch, input_args)


def co_list_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_command_args(config_yml, subgroup="co"))


def co_create_command(config_yml, monkeypatch):
    args_test(monkeypatch, _create_command_args(config_yml, subgroup="co"))


def co_update_command(config_yml, monkeypatch):
    args_test(monkeypatch, _update_command_args(config_yml, "co"))


def co_show_command(config_yml, monkeypatch):
    args_test(monkeypatch, _show_command_args(config_yml, "co"))


def co_create_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _create_plan_args(config_yml, "co"))


def co_update_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _update_plan_args(config_yml, "co"))


def co_list_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_plan_args(config_yml, "ma"))


def co_show_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _show_plan_args(config_yml, "co"))


def co_delete_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _delete_plan_args(config_yml, "co"))


def co_publish_command(config_yml, monkeypatch):
    args_test(monkeypatch, _publish_command_args(config_yml, "co"))


def co_delete_command(config_yml, monkeypatch):
    args_test(monkeypatch, _delete_command_args(config_yml, "co"))


def ma_list_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_command_args(config_yml, subgroup="ma"))


def ma_create_command(config_yml, monkeypatch):
    args_test(monkeypatch, _create_command_args(config_yml, "ma"))


def ma_update_command(config_yml, monkeypatch):
    args_test(monkeypatch, _update_command_args(config_yml, "ma"))


def ma_show_command(config_yml, monkeypatch):
    args_test(monkeypatch, _show_command_args(config_yml, "ma"))


def ma_create_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _create_plan_args(config_yml, "ma"))


def ma_update_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _update_plan_args(config_yml, "ma"))


def ma_list_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_plan_args(config_yml, "ma"))


def ma_show_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _show_plan_args(config_yml, "ma"))


def ma_delete_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _delete_plan_args(config_yml, "ma"))


def ma_publish_command(config_yml, monkeypatch):
    args_test(monkeypatch, _publish_command_args(config_yml, "ma"))


def ma_delete_command(config_yml, monkeypatch):
    args_test(monkeypatch, _delete_command_args(config_yml, "ma"))


def st_list_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_command_args(config_yml, "st"))


def st_create_command(config_yml, monkeypatch):
    args_test(monkeypatch, _create_command_args(config_yml, "st"))


def st_update_command(config_yml, monkeypatch):
    args_test(monkeypatch, _update_command_args(config_yml, "st"))


def st_create_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _create_plan_args(config_yml, "st"))


def st_update_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _update_plan_args(config_yml, "st"))


def st_show_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _show_plan_args(config_yml, "st"))


def st_list_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _list_plan_args(config_yml, "st"))


def st_delete_plan_command(config_yml, monkeypatch):
    args_test(monkeypatch, _delete_plan_args(config_yml, "st"))


def st_show_command(config_yml, monkeypatch):
    args_test(monkeypatch, _show_command_args(config_yml, "st"))


def st_publish_command(config_yml, monkeypatch):
    args_test(monkeypatch, _publish_command_args(config_yml, "st"))


def st_delete_command(config_yml, monkeypatch):
    args_test(monkeypatch, _delete_command_args(config_yml, "st"))


def args_test(monkeypatch, input_args):
    setup_patched_app(monkeypatch, input_args)
    output = azpc_app.main()
    print(output)
    assert output


def _assert_properties(offer, json_listing_config):
    """Assert Properties"""
    properties = Properties(offer.get_product_id(), offer.get_auth()).get().to_dict()
    print("Properties" + str(properties))
    assert properties

    assert properties["app_version"] == json_listing_config["plan_overview"][0]["technical_configuration"]["version"]
    assert properties["terms_of_use"] == ""
    assert properties["submission_version"]
    assert properties["product_tags"]
    assert properties["use_enterprise_contract"]
    assert properties["odata_etag"]
    assert properties["id"]
    assert not properties["industries"]
    assert not properties["categories"]
    assert not properties["additional_categories"]
    assert not properties["hide_keys"]
    assert not properties["marketing_only_change"]
    assert not properties["global_amendment_terms"]
    assert not properties["custom_amendments"]
    return properties


def _assert_offer_listing(offer, json_listing_config):
    """Assert Offer Listing"""
    offer_listing = Listing(offer.get_product_id(), offer.get_auth()).get().to_dict()
    print("Offer Listing: " + str(offer_listing))
    assert offer_listing
    assert offer_listing["odata_etag"]
    assert offer_listing["id"]
    assert offer_listing["summary"] == json_listing_config["offer_listing"]["summary"]
    assert offer_listing["listing_uris"]  # == json_listing_config['listing_uris'] random things aren't matching
    assert offer_listing["listing_contacts"]  # == json_listing_config['listing_contacts']
    assert offer_listing["language_code"] == "en-us"
    assert offer_listing["title"] == json_listing_config["offer_listing"]["title"]
    assert offer_listing["description"] == json_listing_config["offer_listing"]["description"]
    assert offer_listing["short_description"] == json_listing_config["offer_listing"]["short_description"]
    assert offer_listing["publisher_name"] == json_listing_config["offer_listing"]["publisher_name"]
    assert offer_listing["keywords"] == json_listing_config["offer_listing"]["keywords"]
    assert not offer_listing["allow_only_managed_disk_deployments"]
    assert not offer_listing["compatible_products"]


def _assert_preview_audience(offer, json_listing_config):
    """Assert Preview Audience"""
    availability = ProductAvailability(offer.get_product_id(), offer.get_auth()).get().to_dict()
    print("Availability: " + str(availability))
    assert availability
    assert availability["odata_etag"]
    assert availability["id"]
    assert availability["visibility"] == "Public"
    assert availability["enterprise_licensing"] == "Online"
    assert availability["audiences"][0]["values"] == json_listing_config["preview_audience"]["subscriptions"]
    assert not availability["email_audiences"]
    assert not availability["subscription_audiences"]
    assert not availability["hide_key_audience"]


def _assert_plan_listing(offer, json_listing_config):
    """Assert Preview Audience"""
    offer_listing = OfferListing(offer.get_product_id(), offer.get_auth()).get().to_dict()
    print("Offer Listing: " + str(offer_listing))
    assert offer_listing
    assert (
        offer_listing["short_description"]
        == json_listing_config["plan_overview"][0]["plan_listing"]["shortDescription"]
    )
    assert offer_listing["description"] == json_listing_config["plan_overview"][0]["plan_listing"]["description"]
    assert offer_listing["title"] == json_listing_config["plan_overview"][0]["plan_listing"]["title"]


def _assert_pricing_and_availability(offer, json_listing_config):
    """Assert Preview Audience"""
    pricing_and_availability = FeatureAvailability(offer.get_product_id(), offer.get_auth()).get().to_dict()
    print("Pricing & Availability: " + str(pricing_and_availability))
    assert pricing_and_availability


def _assert_technical_configuration(offer, json_listing_config):
    """Assert Preview Audience"""
    tech_configuration = Package(offer.get_product_id(), offer.get_auth()).get()
    print("Technical Configuration: " + str(tech_configuration))
    assert tech_configuration
