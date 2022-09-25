#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Configuration for Package settings in Plan Settings"""
import os
import re
import shutil
import zipfile
from pathlib import Path

import yaml

from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from azureiai.managed_apps.confs.variant.variant_plan_configuration import (
    VariantPlanConfiguration,
)
from azureiai.managed_apps.utils import ACCESS_ID, TENANT_ID
from swagger_client import PackageApi, PackageConfigurationApi
from swagger_client.rest import ApiException


def _inject_pid(file_name_full_path, pid):
    """
    Add PID to ARM template. For more details see this link. GUID registration information on this page is out of date.
    https://docs.microsoft.com/en-us/azure/marketplace/azure-partner-customer-usage-attribution

    This will find and replace the term "pid-GUID-partnercenter". If this is not present in the template, this method
    will have no effect.

    :param file_name_full_path: Full file path to zip of Azure Managed Application.
    :param pid: Managed Application PID to be injected into ARM Template.
    """
    with zipfile.ZipFile(file_name_full_path, "r") as zip_ref:
        zip_ref.extractall(file_name_full_path.replace(".zip", "-temp"))
    with open(file_name_full_path.replace(".zip", "-temp/mainTemplate.json"), "rt", encoding="utf8") as fin:
        data = fin.read()
        data = re.sub(r"pid-(.*)-partnercenter", "pid-" + pid + "-partnercenter", data)

    with open(file_name_full_path.replace(".zip", "-temp/mainTemplate.json"), "wt", encoding="utf8") as fin:
        fin.write(data)

    os.remove(file_name_full_path)
    shutil.make_archive(file_name_full_path.replace(".zip", ""), "zip", file_name_full_path.replace(".zip", "-temp"))
    shutil.rmtree(file_name_full_path.replace(".zip", "-temp"))


class Package(VariantPlanConfiguration):
    """Managed Application Offer - Package Configuration"""

    def __init__(self, product_id, plan_id, authorization, subtype="ma"):
        super().__init__(product_id, plan_id, authorization, subtype)
        self.package_api = PackageApi()
        self.api = PackageConfigurationApi()
        self.module = "Package"

    def get(self):
        """Get Availability for Application"""
        instance_id = self._get_draft_instance_id(module=self.module)
        api_res = self.api.products_product_id_package_configurations_get_by_instance_id_instance_i_dinstance_id_get(
            product_id=self.product_id,
            instance_id=instance_id,
            authorization=self.authorization,
        )
        self.setting_id = api_res["value"][0]["id"]
        return api_res["value"][0]

    def set(
        self,
        app_zip_dir: str,
        file_name: str,
        version: str,
        allow_jit_access: bool = False,
        policies=None,
        resource_type: str = "AzureManagedApplicationPackageConfiguration",
        config_yaml: str = "config.yml",
        allowed_customer_actions: list = None,
        allowed_data_actions: list = None,
        json_config: dict = None,
    ):
        """
        Set Package Configuration

        :param app_zip_dir: directory to managed application zip
        :param file_name: name of managed application zip
        :param version: Version of package
        :param allow_jit_access: boolean enable or disable jit access to customer resources
        :param policies: access policies
        :param resource_type: expecting AzureManagedApplicationPackageConfiguration
        :param config_yaml: configuration file with tenant and aad id
        :param allowed_customer_actions: Control Plane Operation Permissions, single string, ; separated
        :param allowed_data_actions: Control Plane Operation Permissions, single string, ; separated
        :param json_config: listing configuration in json format
        """
        if policies is None:
            policies = []
        if allowed_customer_actions is None:
            allowed_customer_actions = []
        if allowed_data_actions is None:
            allowed_data_actions = []

        post_body = {
            "resourceType": "AzureApplicationPackage",
            "fileName": file_name,
        }

        post_response = self.package_api.products_product_id_packages_post(
            self.authorization, self.product_id, body=post_body
        )

        file_name_full_path = str(Path(app_zip_dir).joinpath(file_name))

        _inject_pid(file_name_full_path, self.product_id)

        upload_response = OfferConfigurations.upload_using_sas(
            post_response.file_sas_uri, Path(app_zip_dir).joinpath(file_name)
        )

        if upload_response != 201:
            raise ConnectionError("Upload via SAS has failed.")
        put_body = {
            "resourceType": "AzureApplicationPackage",
            "fileName": file_name,
            "fileSasUri": post_response.file_sas_uri,
            "State": "Uploaded",
            "@odata.etag": post_response.odata_etag,
        }

        self.package_api.products_product_id_packages_package_id_put(
            authorization=self.authorization,
            product_id=self.product_id,
            package_id=post_response.id,
            body=put_body,
        )

        self._check_upload(post_response)

        settings = self.get()
        odata_etag = settings["@odata.etag"]
        settings_id = settings["id"]

        if resource_type == "AzureSolutionTemplatePackageConfiguration":
            settings = {
                "resourceType": resource_type,
                "version": version,
                "packageReferences": [{"type": "AzureApplicationPackage", "value": post_response.id}],
                "ID": settings_id,
            }
        else:
            plan_config = self._load_plan_config(json_config)
            tenant_id = os.getenv(TENANT_ID, plan_config["technical_configuration"]["tenant_id"])
            access_id = os.getenv(ACCESS_ID, plan_config["technical_configuration"]["authorizations"][0]["id"])
            role = os.getenv("ACCESS_OWNER", plan_config["technical_configuration"]["authorizations"][0]["role"])

            settings = {
                "resourceType": resource_type,
                "version": version,
                "allowJitAccess": allow_jit_access,
                "canEnableCustomerActions": "true",
                "allowedCustomerActions": allowed_customer_actions,
                "allowedDataActions": allowed_data_actions,
                "deploymentMode": "Incremental",
                "publicAzureTenantID": tenant_id,
                "publicAzureAuthorizations": [{"principalID": access_id, "roleDefinitionID": role}],
                "azureGovernmentTenantID": "string",
                "azureGovernmentAuthorizations": [],
                "policies": policies,
                "packageReferences": [{"type": "AzureApplicationPackage", "value": post_response.id}],
                "ID": settings_id,
            }

        try:
            response = self.api.products_product_id_packageconfigurations_package_configuration_id_put(
                authorization=self.authorization,
                if_match=odata_etag,
                product_id=self.product_id,
                package_configuration_id=settings_id,
                body=settings,
            )
        except ApiException as error:
            if "Enter a valid GUID" in bytes.decode(error.body):
                raise ValueError(f"GUID value not valid. Check {config_yaml}") from error
            raise error
        return response

    @staticmethod
    def _load_plan_config(json_config: dict):
        plan_overview = json_config["plan_overview"]
        if isinstance(plan_overview, list):
            return plan_overview[0]
        return plan_overview[next(iter(plan_overview))]

    def _check_upload(self, post_response):
        state = None
        while state != "Processed":
            get_response = self.package_api.products_product_id_packages_package_id_get(
                product_id=self.product_id,
                package_id=post_response.id,
                authorization=self.authorization,
            )
            state = get_response.state
            if state == "ProcessFailed":
                raise ConnectionError("Uploading AMA Zip Failed with State: ProcessedFailed. Check if PID is required")
