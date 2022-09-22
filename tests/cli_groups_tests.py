#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""CLI v2 Test Suite"""
from collections import namedtuple

import requests
import json
from pathlib import Path

from azureiai import azpc_app
from azureiai.managed_apps.confs import Properties, Listing, ProductAvailability
from azureiai.managed_apps.confs.variant import OfferListing, FeatureAvailability, Package
from tests.cli_tests import setup_patched_app

APP_PATH = "tests/sample_app"


def _create_command_args(config_yml, config_json, subgroup):
    return {
        "subgroup": subgroup,
        "command": "create",
        "name": f"test_{subgroup}",
        "config_yml": config_yml,
        "config_json": config_json,
        "app_path": APP_PATH,
    }


def _update_command_args(config_yml, config_json, subgroup):
    return {
        "subgroup": subgroup,
        "command": "update",
        "name": f"test_{subgroup}",
        "config_yml": config_yml,
        "config_json": config_json,
        "app_path": APP_PATH,
    }


def _create_plan_args(config_yml, config_json, subgroup):
    return {
        "subgroup": subgroup,
        "command": "plan",
        "sub_command": "create",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
        "config_json": config_json,
        "app_path": APP_PATH,
    }


def _update_plan_args(config_yml, config_json, subgroup):
    return {
        "subgroup": subgroup,
        "command": "plan",
        "sub_command": "update",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
        "config_json": config_json,
        "app_path": APP_PATH,
    }


def _show_plan_args(config_yml, subgroup):
    input_args = {
        "subgroup": subgroup,
        "command": "plan",
        "plan_command": "show",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
    }
    return input_args


def _list_plan_args(config_yml, subgroup):
    input_args = {
        "subgroup": subgroup,
        "command": "plan",
        "plan_command": "list",
        "name": f"test_{subgroup}",
        "config_yml": config_yml,
    }
    return input_args


def _delete_plan_args(config_yml, subgroup):
    input_args = {
        "subgroup": subgroup,
        "command": "plan",
        "plan_command": "delete",
        "name": f"test_{subgroup}",
        "plan_name": f"test_{subgroup}_plan",
        "config_yml": config_yml,
    }
    return input_args


def _show_command_args(config_yml, subgroup):
    input_args = {"subgroup": subgroup, "command": "show", "name": f"test_{subgroup}", "config_yml": config_yml}
    return input_args


def _list_command_args(config_yml, subgroup):
    return {"subgroup": subgroup, "command": "list", "name": f"test_{subgroup}", "config_yml": config_yml}


def _publish_command_args(config_yml, subgroup):
    input_args = {
        "subgroup": subgroup,
        "command": "publish",
        "name": f"test_{subgroup}",
        "config_yml": config_yml,
        "notification_emails": "dcibs@microsoft.com",
        "app_path": APP_PATH,
    }
    return input_args


def _release_command_args(config_yml, subgroup):
    input_args = {
        "subgroup": subgroup,
        "command": "release",
        "name": f"test_{subgroup}",
        "config_yml": config_yml,
        "notification_emails": "dcibs@microsoft.com",
        "app_path": APP_PATH,
    }
    return input_args


def _delete_command_args(config_yml, subgroup):
    input_args = {"subgroup": subgroup, "command": "delete", "name": f"test_{subgroup}", "config_yml": config_yml}
    return input_args


def vm_create_command(config_yml, json_config, monkeypatch, capsys):
    args = _create_command_args(config_yml, json_config, subgroup="vm")
    args["name"] = "test-vm"
    return args_test(monkeypatch, args, capsys)


def vm_update_command(config_yml, json_config, monkeypatch, capsys):
    class MockResponse:
        def __init__(self):
            self.status_code = 200

        @staticmethod
        def json():
            with open(Path("tests/test_data/vm_show_valid_response.json"), "r", encoding="utf8") as read_file:
                return json.load(read_file)

    def mock_put_request(url, data="", headers="", params="", json=""):
        return MockResponse()

    monkeypatch.setattr(requests, "put", mock_put_request)

    args_test(monkeypatch, _update_command_args(config_yml, json_config, subgroup="vm"), capsys)


def vm_create_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _create_plan_args(config_yml, json_config, subgroup="vm"), capsys)


def vm_update_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _update_plan_args(config_yml, json_config, subgroup="vm"), capsys)


def vm_show_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _show_plan_args(config_yml, "vm"), capsys)


def vm_list_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _list_plan_args(config_yml, "vm"), capsys)


def vm_delete_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _delete_plan_args(config_yml, "vm"), capsys)


def vm_show_command(config_yml, json_config, monkeypatch, capsys):
    args = _show_command_args(config_yml, subgroup="vm")
    args["name"] = "test-vm"
    args["config_json"] = json_config
    args["app_path"] = APP_PATH
    return args_test(monkeypatch, args, capsys)


def vm_list_command(config_yml, monkeypatch, capsys):
    args = _list_command_args(config_yml, subgroup="vm")
    args["name"] = "test-vm"
    return args_test(monkeypatch, args, capsys)


def vm_publish_command(config_yml, json_config, monkeypatch, capsys):
    args = _publish_command_args(config_yml, subgroup="vm")
    args["name"] = "test-vm"
    args["config_json"] = json_config
    args["app_path"] = APP_PATH
    return args_test(monkeypatch, args, capsys)


def vm_delete_command(config_yml, monkeypatch, capsys):
    subgroup = "vm"
    input_args = _delete_command_args(config_yml, subgroup)
    input_args["name"] = "test-vm"
    args_test(monkeypatch, input_args, capsys)


def co_list_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _list_command_args(config_yml, subgroup="co"), capsys)


def co_create_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _create_command_args(config_yml, json_config, subgroup="co"), capsys)


def co_update_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _update_command_args(config_yml, json_config, subgroup="co"), capsys)


def co_show_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _show_command_args(config_yml, "co"), capsys)


def co_create_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _create_plan_args(config_yml, json_config, subgroup="co"), capsys)


def co_update_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _update_plan_args(config_yml, json_config, subgroup="co"), capsys)


def co_list_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _list_plan_args(config_yml, "ma"), capsys)


def co_show_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _show_plan_args(config_yml, "co"), capsys)


def co_delete_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _delete_plan_args(config_yml, "co"), capsys)


def co_publish_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _publish_command_args(config_yml, "co"), capsys)


def co_delete_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _delete_command_args(config_yml, "co"), capsys)


def ma_list_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _list_command_args(config_yml, subgroup="ma"), capsys)


def ma_create_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _create_command_args(config_yml, json_config, subgroup="ma"), capsys)


def ma_update_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _update_command_args(config_yml, json_config, subgroup="ma"), capsys)


def ma_show_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _show_command_args(config_yml, "ma"), capsys)


def ma_create_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _create_plan_args(config_yml, json_config, subgroup="ma"), capsys)


def ma_update_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _update_plan_args(config_yml, json_config, subgroup="ma"), capsys)


def ma_list_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _list_plan_args(config_yml, "ma"), capsys)


def ma_show_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _show_plan_args(config_yml, "ma"), capsys)


def ma_delete_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _delete_plan_args(config_yml, "ma"), capsys)


def ma_publish_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _publish_command_args(config_yml, "ma"), capsys)


def ma_release_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _release_command_args(config_yml, "ma"), capsys)


def ma_delete_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _delete_command_args(config_yml, "ma"), capsys)


def st_list_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _list_command_args(config_yml, "st"), capsys)


def st_create_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _create_command_args(config_yml, json_config, subgroup="st"), capsys)


def st_update_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _update_command_args(config_yml, json_config, subgroup="st"), capsys)


def st_create_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _create_plan_args(config_yml, json_config, subgroup="st"), capsys)


def st_update_plan_command(config_yml, json_config, monkeypatch, capsys):
    args_test(monkeypatch, _update_plan_args(config_yml, json_config, subgroup="st"), capsys)


def st_show_plan_command(config_yml, monkeypatch, capsys):
    return args_test(monkeypatch, _show_plan_args(config_yml, "st"), capsys)


def st_list_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _list_plan_args(config_yml, "st"), capsys)


def st_delete_plan_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _delete_plan_args(config_yml, "st"), capsys)


def st_show_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _show_command_args(config_yml, "st"), capsys)


def st_publish_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _publish_command_args(config_yml, "st"), capsys)


def st_release_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _release_command_args(config_yml, "st"), capsys)


def st_delete_command(config_yml, monkeypatch, capsys):
    args_test(monkeypatch, _delete_command_args(config_yml, "st"), capsys)


def args_test(monkeypatch, input_args, capsys):
    setup_patched_app(monkeypatch, input_args)
    azpc_app.main()
    captured = capsys.readouterr()
    assert captured.out
    return captured.out


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


def _assert_vm_list_all_offers(vm_list, json_listing_config):
    assert len(vm_list) >= 1
    assert vm_list[0]["offerTypeId"] == json_listing_config["offerTypeId"]
    assert vm_list[0]["id"] == json_listing_config["id"]
    assert vm_list[0]["definition"]["displayText"] == json_listing_config["definition"]["displayText"]
    assert vm_list[1]["offerTypeId"] == json_listing_config["offerTypeId"]


def _assert_vm_offer_listing_integration(vm_list):
    assert len(vm_list) >= 1
    for item in vm_list:
        assert item["offerTypeId"] == "microsoft-azure-virtualmachines"


def _assert_vm_empty_listing(vm_list):
    assert len(vm_list) == 0


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


def _assert_vm_show(offer, json_listing_config):
    assert offer["name"] == json_listing_config["definition"]["displayText"]
    assert offer["id"]


def _assert_vm_offer_listing(offer, json_listing_config):
    assert offer["offerTypeId"] == json_listing_config["offerTypeId"]
    assert offer["id"] == json_listing_config["id"]
    assert offer["definition"]["displayText"] == json_listing_config["definition"]["displayText"]

    offer_listing = offer["definition"]["offer"]
    config_offer = json_listing_config["definition"]["offer"]

    assert offer_listing["microsoft-azure-marketplace.title"] == config_offer["microsoft-azure-marketplace.title"]
    assert (
        offer_listing["microsoft-azure-marketplace.offerMarketingUrlIdentifier"]
        == config_offer["microsoft-azure-marketplace.offerMarketingUrlIdentifier"]
    )
    assert offer_listing["microsoft-azure-marketplace.summary"] == config_offer["microsoft-azure-marketplace.summary"]
    assert (
        offer_listing["microsoft-azure-marketplace.longSummary"]
        == config_offer["microsoft-azure-marketplace.longSummary"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.description"]
        == config_offer["microsoft-azure-marketplace.description"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.privacyURL"]
        == config_offer["microsoft-azure-marketplace.privacyURL"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.usefulLinks"][0]
        == config_offer["microsoft-azure-marketplace.usefulLinks"][0]
    )

    assert (
        offer_listing["microsoft-azure-marketplace.engineeringContactName"]
        == config_offer["microsoft-azure-marketplace.engineeringContactName"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.engineeringContactEmail"]
        == config_offer["microsoft-azure-marketplace.engineeringContactEmail"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.engineeringContactPhone"]
        == config_offer["microsoft-azure-marketplace.engineeringContactPhone"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.supportContactName"]
        == config_offer["microsoft-azure-marketplace.supportContactName"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.supportContactEmail"]
        == config_offer["microsoft-azure-marketplace.supportContactEmail"]
    )
    assert (
        offer_listing["microsoft-azure-marketplace.supportContactPhone"]
        == config_offer["microsoft-azure-marketplace.supportContactPhone"]
    )

    # The CPP API creates a copy and stores the uploaded offer listing image elsewhere.
    # This means, the URI of these images will not match the JSON config
    assert offer_listing["microsoft-azure-marketplace.smallLogo"]
    assert offer_listing["microsoft-azure-marketplace.mediumLogo"]
    assert offer_listing["microsoft-azure-marketplace.largeLogo"]
    assert offer_listing["microsoft-azure-marketplace.wideLogo"]
    assert len(offer_listing["microsoft-azure-marketplace.screenshots"]) == 0
    assert len(offer_listing["microsoft-azure-marketplace.videos"]) == 0


def _assert_vm_properties(offer, json_listing_config, detailed=0):
    offer = offer["definition"]["offer"]
    config_offer = json_listing_config["definition"]["offer"]

    assert offer["microsoft-azure-marketplace.termsOfUse"] == config_offer["microsoft-azure-marketplace.termsOfUse"]
    assert (
        config_offer["microsoft-azure-marketplace.categoryMap"][0] in offer["microsoft-azure-marketplace.categoryMap"]
    )
    assert (
        config_offer["microsoft-azure-marketplace.categoryMap"][1] in offer["microsoft-azure-marketplace.categoryMap"]
    )

    # The "show" command returns more details in offer properties
    if detailed:
        assert offer["microsoft-azure-marketplace.universalAmendmentTerms"] == ""
        assert offer["microsoft-azure-marketplace.customAmendments"] == None
        assert offer["microsoft-azure-marketplace.useEnterpriseContract"] == False


def _assert_vm_preview_audience(offer, json_listing_config):
    assert (
        offer["definition"]["offer"]["microsoft-azure-marketplace.allowedSubscriptions"]
        == json_listing_config["definition"]["offer"]["microsoft-azure-marketplace.allowedSubscriptions"]
    )


def _assert_vm_plan_listing(offer, json_listing_config):
    offer_plan = offer["definition"]["plans"][0]
    config_plan = json_listing_config["definition"]["plans"][0]
    assert offer_plan["planId"] == config_plan["planId"]

    assert (
        offer_plan["microsoft-azure-virtualmachines.skuTitle"]
        == config_plan["microsoft-azure-virtualmachines.skuTitle"]
    )
    assert (
        offer_plan["microsoft-azure-virtualmachines.skuSummary"]
        == config_plan["microsoft-azure-virtualmachines.skuSummary"]
    )
    assert (
        offer_plan["microsoft-azure-virtualmachines.skuDescription"]
        == config_plan["microsoft-azure-virtualmachines.skuDescription"]
    )
    assert (
        offer_plan["microsoft-azure-virtualmachines.hideSKUForSolutionTemplate"]
        == config_plan["microsoft-azure-virtualmachines.hideSKUForSolutionTemplate"]
    )
    assert (
        offer_plan["microsoft-azure-virtualmachines.cloudAvailability"]
        == config_plan["microsoft-azure-virtualmachines.cloudAvailability"]
    )
    assert (
        offer_plan["microsoft-azure-virtualmachines.operatingSystemFamily"]
        == config_plan["microsoft-azure-virtualmachines.operatingSystemFamily"]
    )
    assert (
        offer_plan["microsoft-azure-virtualmachines.openPorts"]
        == config_plan["microsoft-azure-virtualmachines.openPorts"]
    )
    assert offer_plan["regions"] == config_plan["regions"]

    offer_plan_vm_sizes = offer_plan["microsoft-azure-virtualmachines.recommendedVMSizes"]
    config_plan_vm_sizes = config_plan["microsoft-azure-virtualmachines.recommendedVMSizes"]
    assert offer_plan_vm_sizes[0] == config_plan_vm_sizes[0]
    assert offer_plan_vm_sizes[1] == config_plan_vm_sizes[1]
    assert offer_plan_vm_sizes[2] == config_plan_vm_sizes[2]
    assert offer_plan_vm_sizes[3] == config_plan_vm_sizes[3]
    assert offer_plan_vm_sizes[4] == config_plan_vm_sizes[4]
    assert offer_plan_vm_sizes[5] == config_plan_vm_sizes[5]
    assert offer_plan["virtualMachinePricing"] == config_plan["virtualMachinePricing"]
    assert offer_plan["virtualMachinePricingV2"] == config_plan["virtualMachinePricingV2"]
