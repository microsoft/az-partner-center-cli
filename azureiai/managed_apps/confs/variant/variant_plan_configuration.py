#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""
Interface for Plan Configuration Settings

Plan configurations must use the variant draft instance to retrieve settings.
"""
import time

from azureiai.managed_apps.confs.offer_configurations import OfferConfigurations


class VariantPlanConfiguration(OfferConfigurations):
    """Managed Application Variant Offer - Interface"""

    def __init__(self, product_id, plan_id, authorization, subtype="ma"):
        super().__init__(product_id, authorization)
        self.subtype = subtype
        self.plan_id = plan_id

    def _get_draft_instance_id(self, module, retry=0):
        """
        Args:
            module:
        """
        time.sleep(3)
        api_response = self.branches_api.products_product_id_branches_get_by_module_modulemodule_get(
            product_id=self.product_id, module=module, authorization=self.authorization
        )
        return self._find_plan(api_response)

    def _find_plan(self, api_response, i=0):
        if i >= len(api_response.value):
            raise ValueError(f"Expected Plan {self.plan_id} not found in {api_response}")
        if api_response.value[i].variant_id == self.plan_id:
            return api_response.value[i].current_draft_instance_id
        return self._find_plan(api_response, i + 1)
