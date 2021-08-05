#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
import os
import pathlib

from azureiai import generate_swagger

SWAGGER_JSON = str(__file__).split("tests")[0] + "Partner_Ingestion_SwaggerDocument.json"

SWAGGER_MODULE_DIR = str(__file__).split("tests")[0]
generate_swagger(SWAGGER_JSON, swagger_module_dir=SWAGGER_MODULE_DIR)
