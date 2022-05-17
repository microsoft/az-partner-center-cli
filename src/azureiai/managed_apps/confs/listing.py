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
        with open(properties, "r", encoding="utf8") as read_file:
            listing_config = json.load(read_file)

            properties = {
                "resourceType": "AzureListing",
                "title": listing_config["offer_listing"]["title"],
                "publisherName": listing_config["offer_listing"]["publisher_name"],
                "summary": listing_config["offer_listing"]["summary"],
                "shortDescription": listing_config["offer_listing"]["short_description"],
                "description": listing_config["offer_listing"]["description"],
                "keywords": listing_config["offer_listing"]["keywords"],
                "listingContacts": listing_config["offer_listing"]["listing_contacts"],
                "listingUris": listing_config["offer_listing"]["listing_uris"],
                "languageCode": "en-us",
                "@odata.etag": odata_etag,
                "id": settings_id,
            }
        return odata_etag, properties, settings_id
