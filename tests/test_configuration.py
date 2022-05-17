#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
""" Azure Managed Application - Unit Tests """
import os
from collections import namedtuple

import pytest
from azureiai.managed_apps.confs import Listing, ListingImage, ProductAvailability, Properties, ResellerConfiguration
from azureiai.managed_apps.confs.variant import FeatureAvailability, OfferListing, Package
from azureiai import RetryException
from swagger_client.rest import ApiException


@pytest.fixture
def availability(ama):
    """Properties PyTest Fixture"""
    return ProductAvailability(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.fixture
def properties(ama):  # noqa
    """Properties PyTest Fixture"""
    return Properties(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.fixture
def listing(ama):
    """Properties PyTest Fixture"""
    return Listing(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.fixture
def listing_image(ama):
    """Listing Image Configuration"""
    return ListingImage(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.fixture
def reseller(ama):
    """Properties PyTest Fixture"""
    return ResellerConfiguration(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.fixture
def feature_availability(ama, plan_name):
    """Properties PyTest Fixture"""
    ama._create_new_plan(plan_name=plan_name)
    return FeatureAvailability(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.fixture
def package(ama, plan_name):
    """Package PyTest Fixture"""
    ama._create_new_plan(plan_name=plan_name)
    return Package(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.fixture
def offer_list(ama, plan_name):
    """Package PyTest Fixture"""
    ama._create_new_plan(plan_name=plan_name)
    return OfferListing(product_id=ama.get_product_id(), authorization=ama.get_auth())


@pytest.mark.integration
def test_force_500(ama, plan_name, monkeypatch):
    """Properties PyTest Fixture"""

    def force_500(
        self,
        method,
        url,
        query_params=None,
        headers=None,
        body=None,
        post_params=None,
        _preload_content=True,
        _request_timeout=None,
    ):
        raise ApiException()

    from swagger_client.rest import RESTClientObject

    monkeypatch.setattr(RESTClientObject, "request", force_500)

    with pytest.raises(RetryException):
        try:
            ama._create_new_plan(plan_name=plan_name)
        except RetryException as exception:
            print(exception)
            raise exception


@pytest.mark.integration
def test_get_availability(availability):
    settings = availability.get()
    assert settings is not None


@pytest.mark.integration
def test_set_use_availability(availability):
    availability.set(visibility="Private", azure_subscription="2eedf122-c960-4ddc-9146-ac93dbf8b2b0")
    settings = availability.get()
    assert settings.visibility == "Private", "Set Action Failed."

    availability.set(azure_subscription="2eedf122-c960-4ddc-9146-ac93dbf8b2b0")
    settings = availability.get()
    assert settings.visibility == "Public", "Set Action Failed."

    availability.set(visibility="Private", azure_subscription="2eedf122-c960-4ddc-9146-ac93dbf8b2b0")
    settings = availability.get()
    assert settings.visibility == "Private", "Set Action Failed."


@pytest.mark.integration
def test_get_properties(properties):
    settings = properties.get()
    assert settings is not None
    assert type(settings.use_enterprise_contract) is bool
    assert not settings.use_enterprise_contract, "Default value was expected to be false."
    assert type(settings.id) is str
    assert type(settings.odata_etag) is str


@pytest.mark.integration
def test_set_use_enterprise_contract(properties):
    categories = ""
    version = "0.0.0"

    properties.set(categories=categories, version=version)
    settings = properties.get()
    assert settings.use_enterprise_contract, "Set Action Failed."

    properties.set(use_enterprise_contract=False, categories=categories, version=version)
    settings = properties.get()
    assert not settings.use_enterprise_contract, "Set Action Failed."

    properties.set(categories=categories, version=version)
    settings = properties.get()
    assert settings.use_enterprise_contract, "Set Action Failed."


@pytest.mark.integration
def test_get_listing(listing):
    settings = listing.get()
    assert settings is not None


@pytest.mark.integration
def test_set_use_listing(listing, app_path_fix, json_listing_config):
    listing.set(properties=os.path.join(app_path_fix, json_listing_config))
    settings = listing.get()
    assert settings is not None, "Set Action Failed."


@pytest.mark.integration
def test_set_listing(listing, listing_image, json_listing_config, app_path_fix):
    listing.set(properties=app_path_fix.joinpath(json_listing_config))
    response = listing_image.set(file_name="r_216_216.png", file_path=app_path_fix, logo_type="AzureLogoLarge")
    assert response is not None
    response = listing_image.set(file_name="r_48_48.png", file_path=app_path_fix, logo_type="AzureLogoSmall")
    assert response is not None
    response = listing_image.set(file_name="r_90_90.png", file_path=app_path_fix, logo_type="AzureLogoMedium")
    assert response is not None
    response = listing_image.set(file_name="r_255_115.png", file_path=app_path_fix, logo_type="AzureLogoWide")
    assert response is not None


@pytest.mark.integration
def test_get_reseller(reseller):
    settings = reseller.get()
    assert settings is not None


@pytest.mark.integration
def test_set_use_reseller(reseller):
    reseller.set()
    settings = reseller.get()
    assert settings is not None, "Set Action Failed."


@pytest.mark.integration
def test_get_feature_availability(feature_availability):
    settings = feature_availability.get()
    assert settings is not None


@pytest.mark.integration
def test_set_use_feature_availability(feature_availability):
    feature_availability.set(azure_subscription="2eedf122-c960-4ddc-9146-ac93dbf8b2b0")
    settings = feature_availability.get()
    assert settings.market_states
    assert settings is not None, "Set Action Failed."


@pytest.mark.integration
def test_get_package(package):
    settings = package.get()
    assert settings is not None


@pytest.mark.integration
def test_set_use_package(package, app_path_fix, app_zip, config_yml):
    version = "0.0.0"
    allow_jit_access = True
    allowed_customer_actions = ["Microsoft.Storage/*;Microsoft.MachineLearningServices/*"]
    allowed_data_actions = ["Microsoft.Storage/*;Microsoft.MachineLearningServices/*"]

    package.set(
        app_zip_dir=app_path_fix,
        file_name=app_zip,
        version=version,
        allow_jit_access=allow_jit_access,
        config_yaml=config_yml,
        allowed_customer_actions=allowed_customer_actions,
        allowed_data_actions=allowed_data_actions,
    )
    settings = package.get()
    assert settings is not None, "Set Action Failed."


@pytest.mark.integration
def test_get_offer_list(offer_list):
    settings = offer_list.get()
    assert settings is not None


@pytest.mark.integration
def test_set_use_offer_list(offer_list):
    properties = {
        "resourceType": "AzureListing",
        "description": "Description for Test",
        "summary": "Summary for Test",
        "languageCode": "en-us",
        "title": "website.Design",
        "shortDescription": "Description",
        "publisherName": "name",
        "keywords": ["design", "simulation", "engineer"],
    }

    offer_list.set(properties=properties)
    settings = offer_list.get()
    assert settings is not None, "Set Action Failed."


@pytest.mark.integration
def test_all_properties(availability, properties, listing, listing_image, reseller, app_path_fix, json_listing_config):
    availability.set(azure_subscription="2eedf122-c960-4ddc-9146-ac93dbf8b2b0")
    industries = ""
    categories = ""
    version = "0.0.0"

    properties.set(industries=industries, categories=categories, version=version)
    listing.set(properties=app_path_fix.joinpath(json_listing_config))
    listing_image.set(file_name="r_216_216.png", file_path=app_path_fix, logo_type="AzureLogoLarge")
    listing_image.set(file_name="r_48_48.png", file_path=app_path_fix, logo_type="AzureLogoSmall")
    listing_image.set(file_name="r_90_90.png", file_path=app_path_fix, logo_type="AzureLogoMedium")
    listing_image.set(file_name="r_255_115.png", file_path=app_path_fix, logo_type="AzureLogoWide")
    reseller.set()
