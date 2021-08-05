#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Variant Configurations are used for setting up new plans within an offer"""
from azureiai.managed_apps.confs.variant.feature_availability import FeatureAvailability
from azureiai.managed_apps.confs.variant.offer_listing import OfferListing
from azureiai.managed_apps.confs.variant.package import Package

__all__ = ["FeatureAvailability", "OfferListing", "Package"]
