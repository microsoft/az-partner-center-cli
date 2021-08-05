#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import pytest
from azureiai import generate_swagger


@pytest.mark.integration
def test_swagger_generate(swagger_json):
    generate_swagger(swagger_json)
