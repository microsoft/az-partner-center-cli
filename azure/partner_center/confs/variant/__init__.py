#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Variant Configurations are used for setting up new plans within an offer"""
from azure.partner_center.confs.variant.feature_availability import FeatureAvailability
from azure.partner_center.confs.variant.offer_listing import OfferListing
from azure.partner_center.confs.variant.package import Package

__all__ = ["FeatureAvailability", "OfferListing", "Package"]
