#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Configurations for Azure Managed Application Plans"""
from azure.partner_center.confs.reseller_configuration import ResellerConfiguration
from azure.partner_center.confs.listing import Listing
from azure.partner_center.confs.listing_image import ListingImage
from azure.partner_center.confs.product_availability import ProductAvailability
from azure.partner_center.confs.properties import Properties

__all__ = [
    "ResellerConfiguration",
    "Listing",
    "ListingImage",
    "ProductAvailability",
    "Properties",
]
