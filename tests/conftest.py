#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Common Fixtures for Pytest Classes"""
from collections import namedtuple
from pathlib import Path

import pytest
import requests
from adal import AuthenticationContext
from azureiai.managed_apps import ManagedApplication
from azureiai.managed_apps.confs import ListingImage
from azureiai.managed_apps.confs.variant import Package
from swagger_client import (
    BranchesApi,
    FeatureAvailabilityApi,
    ListingApi,
    ListingImageApi,
    PackageApi,
    PackageConfigurationApi,
    ProductApi,
    ProductAvailabilityApi,
    PropertyApi,
    ResellerConfigurationApi,
    SubmissionApi,
    VariantApi,
)


@pytest.fixture
def ama_name():
    """Managed Application Offer Name"""
    return "cicd-test-offer-props"


@pytest.fixture
def plan_name():
    """Managed Application Plan Name"""
    return "cicd-test-plan-create-test"


@pytest.fixture
def app_path_fix():
    return Path(__file__).parents[0].joinpath("sample_app")


@pytest.fixture
def app_zip():
    return "sample-app.zip"


@pytest.fixture
def json_listing_config():
    return "sample_app_listing_config.json"


@pytest.fixture
def broken_json_listing_config():
    return "sample_broken_listing_config.json"


@pytest.fixture
def config_yml():
    test_path = Path(__file__).parents[1]
    config_path = test_path.joinpath("config.yml")
    return config_path if config_path.is_file() else test_path.joinpath("template.config.yml")


@pytest.fixture
def manifest_yml():
    return Path(__file__).parents[0].joinpath("sample_app").joinpath("manifest.yml")


@pytest.fixture
def swagger_json():
    return str(Path(__file__).parents[1].joinpath("Partner_Ingestion_SwaggerDocument.json"))


@pytest.mark.integration
@pytest.fixture
def ama(ama_name, config_yml):
    """
    Managed Application Fixture for Testing

    This managed applicaiton is deleted after testing.
    """
    ama = ManagedApplication(ama_name, config_yaml=config_yml)
    ama.create()
    yield ama
    try:
        ama.delete()
    except Exception:
        pass


@pytest.fixture
def template_config():
    return str(__file__).split("tests")[0] + "template.config.yml"


@pytest.fixture
def ama_mock(ama_name, monkeypatch):
    def mock_auth(self):
        return None

    def mock_package_get(self):
        return {"@odata.etag": "not-nothing", "id": "id-something"}

    def mock_products_get(self, authorization, **kwargs):
        variant = namedtuple("variant", ["name", "variant_id", "current_draft_instance_id"])(
            *["test_vm", "abc-123", "draft-instance-id"]
        )
        response_json = namedtuple("response", ["value", "odata_etag", "id"])(
            *[
                [
                    {"name": "test_vm", "id": "abc-123", "variant_id": "abcd1324", "current_draft_instance_id": "123"},
                    {
                        "name": "cicd-test",
                        "id": "abc-123",
                        "variant_id": "abcd1324",
                        "current_draft_instance_id": "123",
                    },
                    {"name": "test_ma", "id": "abc-123", "variant_id": "abcd1324", "current_draft_instance_id": "123"},
                    {"name": "test_st", "id": "abc-123", "variant_id": "abcd1324", "current_draft_instance_id": "123"},
                    {"name": "test_co", "id": "abc-123", "variant_id": "abcd1234", "current_draft_instance_id": "123"},
                ],
                "",
                "",
            ]
        )

        class ResponeJson:
            def __init__(self, response_json):
                self.response_json = response_json
                self.value = "mock_value"

            def to_dict(self):
                return self.response_json._asdict()

        return ResponeJson(response_json)

    def mock_delete(self, product_id, authorization):
        return ""

    def mock_products_post(self, authorization, body):
        response_json = namedtuple("response", ["id"])(*["product-id"])

        class ResponeJson:
            def __init__(self, response_json):
                self.response_json = response_json
                self.id = response_json.id
                self.value = "mock-value"

            def to_dict(self):
                return self.response_json

        return ResponeJson(response_json)

    def mock_variant_response_fa_get(self, authorization, product_id, instance_id, expand):
        variant = namedtuple("a_value", ["id", "odata_etag"])(*["id-not-none", "otag-id"])
        return namedtuple("response", "value")(*[[variant]])

    def mock_branches_get(self, product_id, module, authorization):
        variant = namedtuple("variant", ["variant_id", "current_draft_instance_id"])(*["abc-123", "draft-instance-id"])
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[variant], "", ""])

    def mock_package_config_get(self, product_id, instance_id, authorization):
        return {"value": [{"id": "not_null"}]}

    def mock_variant_post(self, authorization, product_id, body):
        return {"id": "abc-123"}

    def mock_variant_get(self, authorization, product_id, instance_id):
        variant = namedtuple("a_value", ["id", "odata_etag"])(*["id-not-none", "otag-id"])
        return namedtuple("response", "value")(*[[variant]])

    def mock_variant_module_get(self, product_id, authorization, instance_id):
        variant = namedtuple("a_value", ["id", "odata_etag"])(*["id-not-none", "otag-id"])
        return namedtuple("response", "value")(*[[variant]])

    def mock_package_api_get(self, product_id, package_id, authorization):
        return namedtuple("response", ["state", "odata_etag", "id"])(*["Processed", "not-nothing", ""])

    def mock_reseller_response(self, authorization, product_id, body):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_response_products_post(self, authorization, product_id, body):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_post_response_listing(self, authorization, product_id, listing_id, body):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_package_put(self, authorization, product_id, package_id, body):
        return {}

    def mock_variant_response_fa_put(self, authorization, product_id, feature_availability_id, if_match, body, expand):
        variant = namedtuple("a_value", ["id", "odata_etag"])(*["id-not-none", "otag-id"])
        return namedtuple("response", "value")(*[[variant]])

    def mock_pa_response(self, authorization, product_id, if_match, product_availability_id, body):
        variant = namedtuple("a_value", ["id", "odata_etag"])(*["id-not-none", "otag-id"])
        return namedtuple("response", "value")(*[[variant]])

    def mock_variant_response_package(self, authorization, product_id, if_match, package_configuration_id, body):
        variant = namedtuple("a_value", ["id", "odata_etag"])(*["id-not-none", "otag-id"])
        return namedtuple("response", "value")(*[[variant]])

    def mock_response(self, authorization, product_id, body, if_match, listing_id):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_response_submissions_get(self, authorization, product_id):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    def mock_submission_response_post(self, authorization, product_id, body):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_submission_response(self, authorization, product_id, submission_id):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_propery_response(self, authorization, product_id, body, if_match, property_id):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_image_response(self, authorization, product_id, body, if_match, listing_id, image_id):
        return namedtuple("response", ["file_sas_uri", "odata_etag", "id"])(*["", "", ""])

    def mock_package_sas_upload(sas_url, file_name_full_path):
        return 201

    def mock_listing_package_sas_upload(self, sas_url, file_name_full_path):
        return 201

    def mock_put_request(url, data="", headers="", params="", json=""):
        return namedtuple("response", ["status_code"])(*[201])

    def mock_acquire_token_with_client_credentials(self, resource, client_id, client_secret):
        return {"accessToken": "mock-token"}

    def mock_image_listing(self, authorization, product_id, listing_id):
        return namedtuple("response", ["value"])(
            *[namedtuple("value", ["file_name"])(*[namedtuple("file_name", ["file_name"])(*[""])])]
        )

    def mock_app_path(self, authorization, product_id, listing_id):
        return namedtuple("response", ["value"])(
            *[namedtuple("value", ["file_name"])(*[namedtuple("file_name", ["file_name"])(*[""])])]
        )

    monkeypatch.setattr(SubmissionApi, "get", mock_products_get)
    monkeypatch.setattr(VariantApi, "list", mock_products_get)

    monkeypatch.setattr(
        AuthenticationContext, "acquire_token_with_client_credentials", mock_acquire_token_with_client_credentials
    )
    monkeypatch.setattr(ManagedApplication, "get_auth", mock_auth)
    monkeypatch.setattr(VariantApi, "create", mock_variant_post)
    monkeypatch.setattr(ProductApi, "delete", mock_delete)
    monkeypatch.setattr(PackageApi, "create", mock_response_products_post)
    monkeypatch.setattr(PackageApi, "set", mock_package_put)
    monkeypatch.setattr(PackageApi, "get", mock_package_api_get)
    monkeypatch.setattr(PackageConfigurationApi, "get_by", mock_package_config_get)
    monkeypatch.setattr(BranchesApi, "get", mock_branches_get)
    monkeypatch.setattr(Package, "get", mock_package_get)
    monkeypatch.setattr(PackageConfigurationApi, "set", mock_variant_response_package)
    monkeypatch.setattr(FeatureAvailabilityApi, "get_by", mock_variant_response_fa_get)
    monkeypatch.setattr(
        FeatureAvailabilityApi,
        "set",
        mock_variant_response_fa_put,
    )
    monkeypatch.setattr(
        ListingApi,
        "get_by",
        mock_variant_module_get,
    )
    monkeypatch.setattr(ListingApi, "set", mock_response)
    monkeypatch.setattr(
        ProductAvailabilityApi,
        "get_by",
        mock_variant_get,
    )
    monkeypatch.setattr(
        ProductAvailabilityApi,
        "set",
        mock_pa_response,
    )
    monkeypatch.setattr(
        PropertyApi,
        "get_by",
        mock_variant_get,
    )
    monkeypatch.setattr(PropertyApi, "set", mock_propery_response)
    monkeypatch.setattr(
        ListingImageApi, "create", mock_post_response_listing
    )
    monkeypatch.setattr(ListingImage, "upload_using_sas", mock_listing_package_sas_upload)
    monkeypatch.setattr(
        ListingImageApi, "set", mock_image_response
    )
    monkeypatch.setattr(ListingImageApi, "get", mock_image_listing)
    monkeypatch.setattr(
        ResellerConfigurationApi, "create", mock_reseller_response
    )
    monkeypatch.setattr(
        SubmissionApi, "create", mock_submission_response
    )
    monkeypatch.setattr(SubmissionApi, "create", mock_submission_response_post)
    monkeypatch.setattr(SubmissionApi, "list", mock_response_submissions_get)
    monkeypatch.setattr(requests, "put", mock_put_request)
    monkeypatch.setattr(ProductApi, "create", mock_products_post)
    monkeypatch.setattr(ProductApi, "list", mock_products_get)

    ama = ManagedApplication(ama_name, config_yaml=str(__file__).split("tests")[0] + "template.config.yml")
    ama.set_product_id("mock-test")

    return ama
