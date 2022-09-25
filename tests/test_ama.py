#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import shutil
from collections import namedtuple
from pathlib import Path

import pytest

from azure import RetryException
from azure.partner_center.confs import Listing, ListingImage, ResellerConfiguration
from azure.partner_center.confs.offer_configurations import OfferConfigurations
from azure.partner_center.confs.variant import Package
from azure.partner_center.confs.variant.variant_plan_configuration import VariantPlanConfiguration
from azure.partner_center.swagger import download_swagger_jar
from azure.partner_center.utils import get_draft_instance_id
from swagger_client import BranchesApi, PackageApi
from tests.test_ama_mock import create_folders, generate_swagger_testing


@pytest.mark.integration
def test_swagger_integration(swagger_json):
    generate_swagger_testing(swagger_json)

    create_folders()
    swagger_module_dir = "int_test_temp_dir"
    swagger_module_path = Path(swagger_module_dir)
    swagger_module_path.mkdir()

    swagger_jar_path = swagger_module_path.joinpath("bin").joinpath("swagger-codegen-cli.jar")
    download_swagger_jar(swagger_jar_path)

    shutil.rmtree("temp-test")
    shutil.rmtree("int_test_temp_dir")


@pytest.mark.integration
def test_branch_get(monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        variant = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(
            *["variant-id", "draft-instance-id"]
        )
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)
    with pytest.raises(BaseException):
        get_draft_instance_id(product_id="test-id", authorization="auth", module="test-module")


@pytest.mark.integration
def test_listing_image_configuration_error(ama_mock, app_path_fix, monkeypatch):
    def listing_image_set_mock(self, sas_url, file_name_full_path):
        return 400

    monkeypatch.setattr(ListingImage, "upload_using_sas", listing_image_set_mock)
    listing_image = ListingImage(product_id="test-id", authorization="test-auth")
    with pytest.raises(BaseException):
        listing_image.set("216_216.png", app_path_fix, "AzureLogoLarge")


@pytest.mark.integration
def test_listing_configuration_error(app_path_fix, monkeypatch):
    listing = Listing(product_id="test-id", authorization="test-auth")
    with pytest.raises(FileNotFoundError):
        listing.set(properties="not-found")


@pytest.mark.integration
def test_reseller_configuration_error(monkeypatch):
    with pytest.raises(ValueError):
        ResellerConfiguration(product_id="", authorization="").set(reseller_channel_state="NotValid")


@pytest.mark.integration
def test_package_error(app_path_fix, monkeypatch):
    def mock_sas_upload(sas_url, file_name_full_path):
        return 400

    monkeypatch.setattr(OfferConfigurations, "upload_using_sas", mock_sas_upload)

    def mock_response_products_post(self, authorization, product_id, body):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(PackageApi, "products_product_id_packages_post", mock_response_products_post)
    package = Package(product_id="test-id", plan_id="testplan", authorization="test-auth")
    with pytest.raises(BaseException):
        package.set("not-found", str(app_path_fix), version="0.0.0", allow_jit_access=True, policies="")

    with pytest.raises(BaseException):
        package.set("not-found", str(app_path_fix), version="0.0.0", allow_jit_access=True)


@pytest.mark.integration
def test_variant_plan_error(monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    vp_config = VariantPlanConfiguration(product_id="test-id", plan_id="testplan", authorization="test-auth")
    with pytest.raises(ValueError):
        vp_config._get_draft_instance_id(module="")
