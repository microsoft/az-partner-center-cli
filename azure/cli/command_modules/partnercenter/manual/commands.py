# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands import CliCommandType

# pylint: disable=line-too-long
from azure.cli.command_modules.partnercenter._client_factory import cf_partnercenter


def load_command_table(self, _):
    def get_custom_sdk(custom_module, client_factory):
        return CliCommandType(
            operations_tmpl='azure.cli.command_modules.synapse.manual.operations.{}#'.format(custom_module) + '{}',
            client_factory=client_factory,
        )

    partnercenter_ma_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.partnercenter.operations#ManagedAppOperations.{}',
        client_factory=cf_partnercenter)

    partnercenter_plan_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.partnercenter.operations#PlanOperations.{}',
        client_factory=cf_partnercenter)

    partnercenter_st_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.partnercenter.operations#SolutionTemplateOperations.{}',
        client_factory=cf_partnercenter)

    partnercenter_vm_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.partnercenter.operations#VirtualMachineOperations.{}',
        client_factory=cf_partnercenter)

    partnercenter_ct_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.partnercenter.operations#ContainerOperations.{}',
        client_factory=cf_partnercenter)

    with self.command_group('partnercenter ma', command_type=partnercenter_ma_sdk,
                            custom_command_type=get_custom_sdk('ma', cf_partnercenter),
                            client_factory=cf_partnercenter) as g:
        g.command('list', 'list')
        g.show_command('show', 'get')
        g.custom_command('create', 'create', supports_no_wait=True)
        g.custom_command('update', 'update', supports_no_wait=True)
        g.command('delete', 'begin_delete', confirmation=True, supports_no_wait=True)
        g.wait_command('wait')

    with self.command_group('partnercenter ma plan', command_type=partnercenter_plan_sdk,
                            custom_command_type=get_custom_sdk('ma_plan', cf_partnercenter),
                            client_factory=cf_partnercenter) as g:
        g.command('list', 'list')
        g.show_command('show', 'get')
        g.custom_command('create', 'create', supports_no_wait=True)
        g.custom_command('update', 'update', supports_no_wait=True)
        g.command('delete', 'begin_delete', confirmation=True, supports_no_wait=True)
        g.wait_command('wait')

    with self.command_group('partnercenter st', command_type=partnercenter_st_sdk,
                            custom_command_type=get_custom_sdk('st', cf_partnercenter),
                            client_factory=cf_partnercenter) as g:
        g.command('list', 'list')
        g.show_command('show', 'get')
        g.custom_command('create', 'create', supports_no_wait=True)
        g.custom_command('update', 'update', supports_no_wait=True)
        g.command('delete', 'begin_delete', confirmation=True, supports_no_wait=True)
        g.wait_command('wait')

    with self.command_group('partnercenter st plan', command_type=partnercenter_plan_sdk,
                            custom_command_type=get_custom_sdk('st', cf_partnercenter),
                            client_factory=cf_partnercenter) as g:
        g.command('list', 'list')
        g.show_command('show', 'get')
        g.custom_command('create', 'create', supports_no_wait=True)
        g.custom_command('update', 'update', supports_no_wait=True)
        g.command('delete', 'begin_delete', confirmation=True, supports_no_wait=True)
        g.wait_command('wait')

    with self.command_group('partnercenter vm', command_type=partnercenter_vm_sdk,
                            custom_command_type=get_custom_sdk('vm', cf_partnercenter),
                            client_factory=cf_partnercenter) as g:
        g.command('list', 'list')
        g.show_command('show', 'get')
        g.custom_command('create', 'create', supports_no_wait=True)
        g.custom_command('update', 'update', supports_no_wait=True)
        g.command('delete', 'begin_delete', confirmation=True, supports_no_wait=True)
        g.wait_command('wait')

    with self.command_group('partnercenter ct', command_type=partnercenter_ct_sdk,
                            custom_command_type=get_custom_sdk('ct', cf_partnercenter),
                            client_factory=cf_partnercenter) as g:
        g.command('list', 'list')
        g.show_command('show', 'get')
        g.custom_command('create', 'create', supports_no_wait=True)
        g.custom_command('update', 'update', supports_no_wait=True)
        g.command('delete', 'begin_delete', confirmation=True, supports_no_wait=True)
        g.wait_command('wait')
