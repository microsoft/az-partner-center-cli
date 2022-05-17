#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Interface for Offer Configurations"""
import mimetypes
import os
from abc import abstractmethod
from collections import namedtuple

import requests
from azure.storage.blob import ContentSettings  # noqa

from azureiai.managed_apps.utils import get_draft_instance_id
from swagger_client import BranchesApi, ListingApi
from swagger_client.rest import ApiException


class OfferConfigurations:
    """Interface for Offer Configurations"""

    def __init__(self, product_id, authorization):
        self.product_id = product_id
        self.authorization = authorization

        self.branches_api = BranchesApi()
        self.module = None

        self.get_instance = self.instance

        self._settings = None
        self.setting_id = None

    @staticmethod
    def instance(product_id, instance_id, authorization):
        """Abstract Method to get Instance"""
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[product_id], instance_id, authorization])

    def _get_draft_instance_id(self, module, retry=0):
        return get_draft_instance_id(self.product_id, self.authorization, module, retry)

    @staticmethod
    def upload_using_sas(sas_url, file_name_full_path):
        """
        Upload to Azure Storage Via SAS URL

        :param sas_url: Provided by Partner Center
        :param file_name_full_path: file path to upload
        :return: return code status, 201 is expected and indicates success
        """
        file_name_only = os.path.basename(file_name_full_path)
        file_ext = "." + file_name_only.rsplit(".", 1)[1]
        content_type_string = ContentSettings(content_type=mimetypes.types_map[file_ext])

        with open(file_name_full_path, "rb") as file:
            response = requests.put(
                sas_url,
                data=file,
                headers={
                    "content-type": content_type_string.content_type,
                    "x-ms-blob-type": "BlockBlob",
                },
                params={"file": file_name_full_path},
            )
            return response.status_code

    def get(self):
        """Get Settings for Managed Application"""
        instance_id = self._get_draft_instance_id(module=self.module)
        api_response = self.get_instance(
            product_id=self.product_id,
            instance_id=instance_id,
            authorization=self.authorization,
        )
        self.setting_id = api_response.value[0].id
        return api_response.value[0]


class ListingOfferConfigurations(OfferConfigurations):
    """Interface for Listing Offer Configurations"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id=product_id, authorization=authorization)
        self.api = ListingApi()

    def set(self, properties):
        """Set Availability for Application"""
        odata_etag, properties, settings_id = self._get_properties(properties)
        try:
            self.api.products_product_id_listings_listing_id_put(
                authorization=self.authorization,
                if_match=odata_etag,
                product_id=self.product_id,
                listing_id=settings_id,
                body=properties,
            )
        except ApiException as error:
            if "Missing" in bytes.decode(error.body):
                raise ValueError(f"{bytes.decode(error.body)} missing from {properties}") from error
            raise error

    @abstractmethod
    def _get_properties(self, properties):
        """Load properties from file or dict."""
