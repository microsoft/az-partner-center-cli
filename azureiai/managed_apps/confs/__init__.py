#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Configurations for Azure Managed Application Plans"""
from azureiai.managed_apps.confs.listing import Listing
from azureiai.managed_apps.confs.listing_image import ListingImage
from azureiai.managed_apps.confs.product_availability import ProductAvailability
from azureiai.managed_apps.confs.properties import Properties
from azureiai.managed_apps.confs.reseller_configuration import ResellerConfiguration

__all__ = [
    "ResellerConfiguration",
    "Listing",
    "ListingImage",
    "ProductAvailability",
    "Properties",
]
