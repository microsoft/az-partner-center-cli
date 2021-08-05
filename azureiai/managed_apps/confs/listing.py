#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Listing Configuration for Offer Settings"""
import json
import os

from azureiai.managed_apps.confs.offer_configurations import ListingOfferConfigurations


class Listing(ListingOfferConfigurations):
    """Managed Application Offer - Listing Configuration"""

    def __init__(self, product_id, authorization):
        super().__init__(product_id, authorization)
        self.module = "Listing"
        self.get_instance = self.api.products_product_id_listings_get_by_instance_id_instance_i_dinstance_id_get

        self._settings = None
        self.settings_id = None

    def set(self, properties="listing_config.json"):
        """Set Availability for Application

        :param properties: path to configuration json
        """
        super().set(properties=properties)

    def _get_properties(self, properties):
        if not os.path.isfile(properties):
            raise FileNotFoundError("Listing Configuration Not Found")
        settings = self.get()
        odata_etag = settings.odata_etag
        settings_id = settings.id
        with open(properties, "r") as read_file:
            listing_config = json.load(read_file)

            properties = {
                "resourceType": "AzureListing",
                "summary": listing_config["summary"],
                "listingUris": listing_config["listing_uris"],
                "listingContacts": listing_config["listing_contacts"],
                "languageCode": "en-us",
                "title": listing_config["title"],
                "description": listing_config["description"],
                "shortDescription": listing_config["short_description"],
                "publisherName": "Microsoft Corp.",
                "keywords": listing_config["keywords"],
                "@odata.etag": odata_etag,
                "id": settings_id,
            }
        return odata_etag, properties, settings_id
