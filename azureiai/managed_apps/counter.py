#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""API Response Counter"""


def inc_counter(api_response):
    """
    Find the Response Value to return

    :param api_response:
    :return:
    """
    i = 0
    if api_response.value[i].variant_id is None:
        i += 1
    if api_response.value[i].variant_id == "testdrive":
        i += 1
    return i
