#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import json
import os
import shutil
from collections import namedtuple
from pathlib import Path

import pytest
from azureiai import RetryException
from azureiai.managed_apps import ManagedApplication
from azureiai.managed_apps.confs import Listing, ListingImage, ResellerConfiguration
from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from azureiai.managed_apps.confs.variant import Package
from azureiai.managed_apps.confs.variant.variant_plan_configuration import VariantPlanConfiguration
from azureiai.managed_apps.swagger import download_swagger_jar
from azureiai.managed_apps.utils import get_draft_instance_id
from swagger_client import BranchesApi, PackageApi, SubmissionApi
from tests.test_ama_mock import create_folders, generate_swagger_testing


@pytest.mark.integration
def test_ama_create(ama):
    assert ama is not None


@pytest.mark.integration
def test_create_plan(ama, plan_name):
    ama._create_new_plan(plan_name)


@pytest.mark.integration
def test_ama_delete(ama_name, config_yml):
    ama = ManagedApplication(
        ama_name,
        config_yaml=config_yml,
    )
    ama.create()
    product_id = ama.get_product_id()
    ama.set_product_id(product_id)
    assert product_id == ama.get_product_id()
    ama.delete()


@pytest.mark.integration
def test_ama_delete_no_create(ama_name, config_yml):
    ama = ManagedApplication(
        ama_name,
        config_yaml=config_yml,
    )
    ama.get_product_id()
    ama.delete()


@pytest.mark.integration
def test_ama_publish(ama, plan_name, app_path_fix, app_zip, json_listing_config, config_yml):
    try:
        prepared = ama.prepare_publish(
            plan_name=plan_name,
            app_path=app_path_fix,
            app=app_zip,
            json_listing_config=json_listing_config,
            config_yml=config_yml,
        )
    except ValueError as error:
        raise ValueError(f"{app_path_fix}{os.path.sep}{json_listing_config}") from error
    assert prepared

    submission = ama.submission_status()
    assert submission

    published = ama.publish()
    assert published
    assert published.id


@pytest.mark.integration
def test_ama_update_plan(ama, plan_name, app_path_fix, app_zip, json_listing_config, config_yml):
    prepared = ama.prepare_publish(
        plan_name=plan_name,
        app_path=app_path_fix,
        app=app_zip,
        json_listing_config=json_listing_config,
        config_yml=config_yml,
    )
    assert prepared

    submission = ama.submission_status()
    assert submission

    with open(Path(app_path_fix).joinpath(json_listing_config), "r") as read_file:
        json_config = json.load(read_file)

    json_config["version"] = "0.0.1"
    ama._set_technical_configuration(json_config, app_zip, app_path_fix, config_yml)

    published = ama.publish()
    assert published
    assert published.id


@pytest.mark.integration
def test_ama_update_existing(ama, plan_name, app_path_fix, app_zip, json_listing_config, config_yml):
    with open(Path(app_path_fix).joinpath(json_listing_config), "r") as read_file:
        json_config = json.load(read_file)
    json_config["version"] = "0.0.3"
    ama.set_product_id("411968ab-9f17-40dd-8378-f22d8e39acbb")
    ama.update(json_listing_config=json_listing_config, app=app_zip, app_path=app_path_fix, config_yml=config_yml)


@pytest.mark.integration
def test_ama_2nd_plan(ama, plan_name, app_path_fix, app_zip, json_listing_config, config_yml):
    prepared = ama.prepare_publish(
        plan_name=plan_name,
        app_path=app_path_fix,
        app=app_zip,
        json_listing_config=json_listing_config,
        config_yml=config_yml,
    )
    assert prepared

    submission = ama.submission_status()
    assert submission

    published = ama.publish()
    assert published
    assert published.id

    ama._create_new_plan(plan_name=plan_name + "2")


@pytest.mark.integration
def test_ama_get_offers(ama):
    offers = ama.get_offers()
    assert offers.value


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
def test_ama_publish_prepare_error(
    ama, plan_name, app_path_fix, app_zip, json_listing_config, broken_json_listing_config, template_config
):
    with pytest.raises(FileNotFoundError):
        assert ama.prepare_publish(
            plan_name=plan_name,
            app="not-found",
            app_path=app_path_fix,
            json_listing_config=json_listing_config,
            config_yml=template_config,
        )

    with pytest.raises(FileNotFoundError):
        assert ama.prepare_publish(
            plan_name=plan_name,
            app_path=app_path_fix,
            app=app_zip,
            json_listing_config=broken_json_listing_config,
            config_yml=template_config,
        )
    with pytest.raises(FileNotFoundError):
        assert ama.prepare_publish(
            plan_name=plan_name,
            app_path=app_path_fix,
            app=app_zip,
            json_listing_config=broken_json_listing_config,
            config_yml=template_config,
        )
    with pytest.raises(FileNotFoundError):
        assert ama.prepare_publish(
            plan_name=plan_name,
            app_path=app_path_fix,
            app=app_zip,
            json_listing_config=broken_json_listing_config,
            config_yml=template_config,
        )
    with pytest.raises(FileNotFoundError):
        assert ama.prepare_publish(
            plan_name=plan_name,
            app_path=app_path_fix,
            app=app_zip,
            json_listing_config=broken_json_listing_config,
            config_yml=template_config,
        )
    with pytest.raises(FileNotFoundError):
        assert ama.prepare_publish(
            plan_name=plan_name,
            app_path=app_path_fix,
            app=app_zip,
            config_yml=template_config,
        )


@pytest.mark.integration
def test_ama_get_draft_instance_id_retry(ama, monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    with pytest.raises(BaseException):
        ama._get_draft_instance_id(module="")

    def mock_branches_get(self, product_id, module, authorization):
        variant = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(
            *["variant-id", "draft-instance-id"]
        )
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant], "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)


@pytest.mark.integration
def test_ama_promote(ama, monkeypatch):
    def mock_branches_get(self, product_id, submission_id, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(SubmissionApi, "products_product_id_submissions_submission_id_promote_post", mock_branches_get)

    ama.promote()


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
    package = Package(product_id="test-id", authorization="test-auth")
    with pytest.raises(BaseException):
        package.set("not-found", str(app_path_fix), version="0.0.0", allow_jit_access=True, policies="")

    with pytest.raises(BaseException):
        package.set("not-found", str(app_path_fix), version="0.0.0", allow_jit_access=True)


@pytest.mark.integration
def test_variant_plan_error(monkeypatch):
    def mock_branches_get(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    vp_config = VariantPlanConfiguration(product_id="test-id", authorization="test-auth")
    with pytest.raises(RetryException):
        vp_config._get_draft_instance_id(module="")

    def mock_branches_error(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_error)
    with pytest.raises(BaseException):
        vp_config._get_draft_instance_id(module="")

    def mock_branches_get(self, product_id, module, authorization):
        variant_1 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*[None, "draft-instance-id"])
        variant_2 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(
            *["testdrive", "draft-instance-id"]
        )
        variant_3 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*["abc123", "draft-instance-id"])
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant_1, variant_2, variant_3], "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    vp_config._get_draft_instance_id(module="")


@pytest.mark.integration
def test_ama_retry(monkeypatch, ama_name, config_yml):
    ama = ManagedApplication(
        ama_name,
        config_yaml=config_yml,
    )

    def mock_branches_get(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    with pytest.raises(RetryException):
        ama._get_variant_draft_instance_id(module="")

    def mock_branches_error(self, product_id, module, authorization):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_error)
    with pytest.raises(RetryException):
        ama._get_variant_draft_instance_id(module="")

    def mock_branches_get(self, product_id, module, authorization):
        variant_1 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*[None, "draft-instance-id"])
        variant_2 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(
            *["testdrive", "draft-instance-id"]
        )
        variant_3 = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*["abc123", "draft-instance-id"])
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant_1, variant_2, variant_3], "", ""])

    monkeypatch.setattr(BranchesApi, "products_product_id_branches_get_by_module_modulemodule_get", mock_branches_get)

    ama._get_variant_draft_instance_id(module="")
