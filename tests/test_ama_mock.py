#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import os
import shutil
from collections import namedtuple
from pathlib import Path

import pytest
import wget
from adal import AuthenticationContext
from azure import generate_swagger
from azure.partner_center.confs import Listing, ListingImage, ResellerConfiguration
from azure.partner_center.confs.offer_configurations import OfferConfigurations
from azure.partner_center.confs.variant import Package
from azure.partner_center.confs.variant.variant_plan_configuration import VariantPlanConfiguration
from azure.partner_center.offer import Offer
from azure.partner_center.swagger import download_swagger_jar
from azure.partner_center.utils import get_draft_instance_id
from swagger_client import BranchesApi, PackageConfigurationApi, ResellerConfigurationApi, ProductApi


def test_variant_plan_mock(monkeypatch):

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    vp_config = VariantPlanConfiguration(product_id="test-id", plan_id="abc-123", authorization="test-auth")
    vp_config._get_draft_instance_id(module="")


def test_reseller_configuration_mock(ama_mock, monkeypatch):
    def mock_branches_get(self, product_id, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(ResellerConfigurationApi, "products_product_id_reseller_configuration_get", mock_branches_get)

    response = ResellerConfiguration(product_id="", authorization="").get()
    assert response


def test_reseller_configuration_mock_error(ama_mock, monkeypatch):
    with pytest.raises(ValueError):
        ResellerConfiguration(product_id="", authorization="").set(reseller_channel_state="NotValid")


def test_offer_config_mock(monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    offer_config = OfferConfigurations("test-id", "no-auth")
    with pytest.raises(BaseException):
        offer_config._get_draft_instance_id(module="test-module")

    def mock_branches_get(self, product_id, module, authorization):
        variant = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(
            *["variant-id", "draft-instance-id"]
        )
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant], "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)


def create_folders():
    """
    Create Folders for testing
    """
    if not os.path.isdir("temp-test"):
        os.mkdir("temp-test")
    if not os.path.isdir("temp-test/bin"):
        os.mkdir("temp-test/bin")
    if not os.path.isdir("test_temp_dir"):
        os.mkdir("test_temp_dir")
    if not os.path.isdir("test_temp_dir/bin"):
        os.mkdir("test_temp_dir/bin")
    if not os.path.isdir("temp-test/swagger_client"):
        os.mkdir("temp-test/swagger_client")


def generate_swagger_testing(swagger_json):
    """
    Generate Swagger Spec for Testing

    :param swagger_json: path to swagger json
    """
    with pytest.raises(FileNotFoundError):
        generate_swagger(swagger_json="", swagger_module_dir="test_temp_dir", swagger_dir="not_swagger")
    create_folders()
    generate_swagger(swagger_json=swagger_json)
    shutil.rmtree("temp-test")
    shutil.rmtree("test_temp_dir")


def test_swagger_generate_mock(monkeypatch, swagger_json):
    def wget_download_mock(url, out):
        return {}

    monkeypatch.setattr(wget, "download", wget_download_mock)

    generate_swagger_testing(swagger_json)


def test_swagger_download_mock(monkeypatch, swagger_json):
    def wget_download_mock(url, out):
        return {}

    monkeypatch.setattr(wget, "download", wget_download_mock)

    def ssh_move_mock(src, dst):
        return {}

    monkeypatch.setattr(shutil, "move", ssh_move_mock)

    download_swagger_jar(Path("test.jar"))


def test_offer_get_auth_mock(template_config, monkeypatch):
    def request_post_mock(self, resource, client_id, client_secret):
        return {"accessToken": "test-token"}

    monkeypatch.setattr(AuthenticationContext, "acquire_token_with_client_credentials", request_post_mock)

    offer = Offer("test")
    offer.get_auth()


def test_package_get_mock(monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        variant = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*["abc-123", "draft-instance-id"])
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant], "", ""])

    def mock_package_config_get(self, product_id, instance_id, authorization):
        return {"value": [{"id": "not_null"}]}

    monkeypatch.setattr(
        PackageConfigurationApi,
        "products_product_id_package_configurations_get_by_instance_id_instance_i_dinstance_id_get",
        mock_package_config_get,
    )
    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    package = Package(product_id="test-id", plan_id="abc-123", authorization="test-auth")
    response = package.get()
    assert response


def test_package_mock_error(ama_mock, app_path_fix, monkeypatch):
    def mock_sas_upload(sas_url, file_name_full_path):
        return 400

    monkeypatch.setattr(OfferConfigurations, "upload_using_sas", mock_sas_upload)

    package = Package(product_id="test-id", plan_id="abc-123", authorization="test-auth")
    with pytest.raises(BaseException):
        package.set("not-found", app_path_fix, version="0.0.0", allow_jit_access=True, policies="")

    with pytest.raises(BaseException):
        package.set("not-found", app_path_fix, version="0.0.0", allow_jit_access=True)


def test_listing_image_configuration_mock_error(ama_mock, app_path_fix, monkeypatch):
    def listing_image_set_mock(self, sas_url, file_name_full_path):
        return 400

    monkeypatch.setattr(ListingImage, "upload_using_sas", listing_image_set_mock)
    listing_image = ListingImage(product_id="test-id", authorization="test-auth")
    with pytest.raises(BaseException):
        listing_image.set("216_216.png", app_path_fix, "AzureLogoLarge")


def test_listing_configuration_mock_error(ama_mock, app_path_fix, monkeypatch):
    listing = Listing(product_id="test-id", authorization="test-auth")
    with pytest.raises(FileNotFoundError):
        listing.set(properties="not-found")


def mock_branches_get(self, product_id, module, authorization):
    variant_1 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*[None, "draft-instance-id"])
    variant_2 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*["testdrive", "draft-instance-id"])
    variant_3 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*["abc-123", "draft-instance-id"])
    return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant_1, variant_2, variant_3], "", ""])


def test_variant_plan_mock_error(monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    vp_config = VariantPlanConfiguration(product_id="test-id", plan_id="abc-123", authorization="test-auth")
    with pytest.raises(BaseException):
        vp_config._get_draft_instance_id(module="")


def test_offer_get_product_id(monkeypatch):
    def mock_create(self):
        self._ids["product_id"] = "sample-product-id"
        return namedtuple("response", ["id", "odata_etag"])(*["sample-product-id", ""])

    monkeypatch.setattr(Offer, "create", mock_create)

    def mock_auth(self):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(Offer, "get_auth", mock_auth)

    def mock_products_get(self, authorization, filter):
        class mock_response:
            def to_dict(self):
                return {"value": []}

        return mock_response()

    monkeypatch.setattr(ProductApi, "products_get", mock_products_get)

    offer = Offer(name="test-offer")
    product_id = offer.get_product_id()
    assert product_id == ""


def test_branch_get_mock(monkeypatch):
    OfferConfigurations.instance("1", "2", "3")


def test_branch_get_mock(monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        variant = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(
            *["variant-id", "draft-instance-id"]
        )
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant], "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)
    get_draft_instance_id(product_id="test-id", authorization="auth", module="test-module")

    def mock_branches_get(self, product_id, module, authorization):
        variant = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(
            *["variant-id", "draft-instance-id"]
        )
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)
    with pytest.raises(BaseException):
        get_draft_instance_id(product_id="test-id", authorization="auth", module="test-module")
