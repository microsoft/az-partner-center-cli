#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Common Utilities and Constants"""
from time import sleep

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


def get_variant_draft_instance_id(plan_id, product_id, authorization, module: str):
    """
    Common Static Method for Retrieving Variant Draft Instance ID for applications or properties

    :param plan_id: Application Plan ID
    :param product_id: Application Product ID
    :param authorization: Authorization object
    :param module: name of draft instance to look up
    :return: response
    """
    sleep(3)
    api_response = BRANCHES_API.products_product_id_branches_get_by_module_modulemodule_get(
        product_id=product_id,
        module=module,
        authorization=authorization,
    )
    return _find_plan(plan_id, api_response)


def _find_plan(plan_id, api_response, i=0):
    if api_response.value[i].variant_id == plan_id:
        return api_response.value[i].current_draft_instance_id
    return _find_plan(plan_id, api_response, i + 1)


ACCESS_ID = "AZURE_CLIENT_ID"
TENANT_ID = "AZURE_TENANT_ID"
AAD_ID = "AZURE_CLIENT_ID"
AAD_CRED = "AZURE_CLIENT_SECRET"
