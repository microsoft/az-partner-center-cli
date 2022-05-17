import requests

from swagger_client import ApiClient


class OffersApi(object):
    """Virtual Machine Offer API"""

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_offer(self, resource_path, body, headers):
        return requests.put(resource_path, body, headers=headers)
