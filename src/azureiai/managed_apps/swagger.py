#  ---------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  ---------------------------------------------------------
"""Swagger Functions"""
import shutil
from posixpath import join as url_join

import wget


def download_swagger_jar(swagger_jar_path, swagger_version="3.0.22"):
    """
    Download Swagger Jar

    :param swagger_jar_path: path to jar
    :param swagger_version: version of swagger
    """
    if not swagger_jar_path.is_file():
        url = url_join(
            "https://repo1.maven.org/maven2",
            "io/swagger/codegen/v3/swagger-codegen-cli",
            swagger_version,
            f"swagger-codegen-cli-{swagger_version}.jar",
        )
        wget.download(url, swagger_jar_path.name)
        shutil.move(swagger_jar_path.name, swagger_jar_path.parent)
