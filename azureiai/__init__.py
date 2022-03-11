#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Azure Industrial AI"""
import os
import shutil
import subprocess
from pathlib import Path
from tempfile import mkdtemp

__all__ = ["RetryException"]


def generate_swagger(swagger_json, swagger_module_dir="./", output=True, swagger_dir="swagger_client"):
    """
    Generate Swagger Source from Swagger JSON

    :param swagger_json: Path to Swagger JSON OpenAPI V3 file. Required.
    :param swagger_module_dir: Location to drop new swagger_client directory, must not currently exist. Default: "./"
    :param output: Print Swagger Jar output to Console. Default: False
    """
    swagger_client_path = Path(__file__).parents[1].joinpath(swagger_dir)
    swagger_jar_path = Path(__file__).parents[1].joinpath("bin").joinpath("swagger-codegen-cli-3.0.29.jar")
    if not swagger_client_path.is_dir():
        if not os.path.exists(swagger_json) or not os.path.exists(swagger_jar_path.__str__()):
            raise FileNotFoundError("Missing Swagger Spec: ", swagger_json, swagger_jar_path.__str__())

        tmp_dir = mkdtemp()

        with subprocess.Popen(  # nosec
            [
                "java",
                "-jar",
                str(swagger_jar_path),
                "generate",
                "-i",
                swagger_json,
                "-l",
                "python",
                "-o",
                tmp_dir,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        ) as my_out:
            if output:
                stdout, stderr = my_out.communicate()

                print(stdout.decode("utf-8"))
                print(stderr)
            shutil.move(Path(tmp_dir).joinpath("swagger_client").__str__(), swagger_module_dir)


class RetryException(Exception):
    """Retry Exception"""

    def __str__(self):
        return "Failed after retrying many times."
