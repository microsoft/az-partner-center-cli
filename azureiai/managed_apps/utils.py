#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Common Utilities and Constants"""
from azureiai.managed_apps.counter import inc_counter
from swagger_client import BranchesApi

BRANCHES_API = BranchesApi()


def get_draft_instance_id(product_id, authorization, module: str, retry: int = 0):
    """
    Common Static Method for Retrieving Draft Instance ID for applications or properties

    :param product_id: Managed Application Product ID
    :param authorization: Authorization object
    :param module: name of draft instance to look up
    :param retry: retry attempt number, will retry 3 times before failing
    :return: response
    """
    api_response = BRANCHES_API.products_product_id_branches_get_by_module_modulemodule_get(
        product_id=product_id, module=module, authorization=authorization
    )
    if not api_response.value:
        if retry < 5:
            return get_draft_instance_id(product_id, authorization, module=module, retry=retry + 1)
        raise ConnectionError("Retry Failed")
    return api_response.value[0].current_draft_instance_id


def get_variant_draft_instance_id(product_id, authorization, module: str, retry: int = 0):
    """
    Common Static Method for Retrieving Variant Draft Instance ID for applications or properties

    :param product_id: Managed Application Product ID
    :param authorization: Authorization object
    :param module: name of draft instance to look up
    :param retry: retry attempt number, will retry 3 times before failing
    :return: response
    """
    api_response = BRANCHES_API.products_product_id_branches_get_by_module_modulemodule_get(
        product_id=product_id,
        module=module,
        authorization=authorization,
    )
    if not api_response.value:
        if retry < 3:
            return get_variant_draft_instance_id(product_id, authorization, module=module, retry=retry + 1)
        raise ConnectionError("Retry Failed")
    i = inc_counter(api_response)
    return api_response.value[i].current_draft_instance_id


ACCESS_ID = "ACCESS_ID"
TENANT_ID = "TENANT_ID"
AAD_ID = "AAD_ID"
AAD_CRED = "AAD_SECRET"
