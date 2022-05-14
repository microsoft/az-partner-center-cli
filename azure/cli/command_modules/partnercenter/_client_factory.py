# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def cf_partnercenter(cli_ctx, **_):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.mgmt.resource import SubscriptionClient
    return get_mgmt_service_client(cli_ctx, SubscriptionClient, subscription_bound=False)


def cf_registration_ma(cli_ctx, _):
    return cf_managedservices(cli_ctx)


def cf_registration_st(cli_ctx, _):
    return cf_managedservices(cli_ctx)


def cf_registration_vm(cli_ctx, _):
    return cf_managedservices(cli_ctx)
