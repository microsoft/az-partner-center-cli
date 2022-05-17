#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Interface for Plan Configuration Settings

Plan configurations must use the variant draft instance to retrieve settings.
"""
from azureiai import RetryException
from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations
from azureiai.managed_apps.counter import inc_counter


class VariantPlanConfiguration(OfferConfigurations):
    """Managed Application Variant Offer - Interface"""

    def _get_draft_instance_id(self, module, retry=0):
        """
        Args:
            module:
        """
        api_response = self.branches_api.products_product_id_branches_get_by_module_modulemodule_get(
            product_id=self.product_id, module=module, authorization=self.authorization
        )
        if not api_response.value:
            if retry < 3:
                return self._get_draft_instance_id(module=module, retry=retry + 1)
            raise RetryException("Retry Failed")
        i = inc_counter(api_response)
        return api_response.value[i].current_draft_instance_id
