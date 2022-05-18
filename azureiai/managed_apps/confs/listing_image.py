#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Managed Application Offer - Listing Image Configuration"""
import uuid
from pathlib import Path

from azureiai.managed_apps.confs.listing import Listing
from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from swagger_client import ListingImageApi


class ListingImage(OfferConfigurations):
    """Managed Application Offer - Listing Image Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)

        self.listing_image_api = ListingImageApi()
        self.list = Listing(product_id, authorization)

        self._settings = None
        self.settings_id = None

    def set(self, file_name, file_path, logo_type):
        """
        Set Listing Image Configuration

        :param file_name: name of file
        :param file_path: path to file
        :param logo_type: image logo type: [large, medium, small, wide]
        :return: api_response
        """

        api_response = self.listing_image_api.products_product_id_listings_listing_id_images_get(
            authorization=self.authorization, product_id=self.product_id, listing_id=self.list.get().id
        )
        for value in api_response.value:
            if value.file_name == file_name:
                self.listing_image_api.products_product_id_listings_listing_id_images_image_id_delete(
                    authorization=self.authorization,
                    product_id=self.product_id,
                    listing_id=self.list.get().id,
                    image_id=value.id,
                )

        image_id = str(uuid.uuid4())

        body = {
            "resourceType": "ListingImage",
            "fileName": file_name,
            "type": logo_type,
            "state": "PendingUpload",
            "order": 0,
            "id": image_id,
        }

        api_response = self.listing_image_api.products_product_id_listings_listing_id_images_post(
            authorization=self.authorization,
            product_id=self.product_id,
            listing_id=self.list.get().id,
            body=body,
        )
        status_code = self.upload_using_sas(api_response.file_sas_uri, Path(file_path).joinpath(file_name))
        if status_code != 201:
            raise ConnectionError("Upload via SAS Failed")
        body = {
            "resourceType": "ListingImage",
            "fileName": file_name,
            "type": logo_type,
            "fileSasUri": api_response.file_sas_uri,
            "state": "Uploaded",
            "order": 0,
            "@odata.etag": api_response.odata_etag,
            "id": api_response.id,
        }

        return self.listing_image_api.products_product_id_listings_listing_id_images_image_id_put(
            authorization=self.authorization,
            if_match=api_response.odata_etag,
            product_id=self.product_id,
            listing_id=self.list.get().id,
            image_id=api_response.id,
            body=body,
        )
