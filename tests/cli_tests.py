import argparse
from collections import namedtuple
import json
import sys

import pytest
from azureiai import ama_app
from swagger_client.api.submission_api import SubmissionApi
from swagger_client.rest import ApiException


def bad_command_integration(monkeypatch):
    def get_args(self):
        return argparse.Namespace(command="not_command"), argparse.Namespace()

    monkeypatch.setattr(argparse.ArgumentParser, "parse_known_args", get_args)
    with pytest.raises(KeyError):
        ama_app.main()


def list_command(config_yml, monkeypatch):
    input_args = {"command": "list", "ama_name": "cicd-test", "config_yml": config_yml}
    setup_patched_app(monkeypatch, input_args)
    output = ama_app.main()
    assert output


def create_then_delete(config_yml, monkeypatch, manifest_yml):
    create_args = {"command": "create", "ama_name": "cicd-test", "config_yml": config_yml, "manifest_yml": manifest_yml}
    setup_patched_app(monkeypatch, create_args)
    product_id_json = json.loads(ama_app.main())
    assert product_id_json
    product_id = product_id_json["product_id"]
    delete_args = {"command": "delete", "product_id": product_id, "config_yml": config_yml}
    setup_patched_app(monkeypatch, delete_args)
    ama_app.main()


def create_publish_delete(config_yml, manifest_yml, monkeypatch):
    create_args = {"command": "create", "ama_name": "cicd-test", "config_yml": config_yml, "manifest_yml": manifest_yml}
    setup_patched_app(monkeypatch, create_args)
    product_id_json = json.loads(ama_app.main())
    assert product_id_json
    product_id = product_id_json["product_id"]
    offer_id = product_id_json["offer_id"]
    publish_args = {
        "command": "publish",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "offer_id": offer_id,
        "config_yml": config_yml,
        "manifest_yml": manifest_yml,
    }
    setup_patched_app(monkeypatch, publish_args)
    ama_app.main()
    status_args = {
        "command": "status",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "config_yml": config_yml,
    }
    setup_patched_app(monkeypatch, status_args)
    status = ama_app.main()
    assert status
    delete_args = {"command": "delete", "product_id": product_id, "config_yml": config_yml}
    setup_patched_app(monkeypatch, delete_args)
    ama_app.main()


def update_ama(config_yml, manifest_yml, monkeypatch):
    update_args = {
        "command": "update",
        "ama_name": "cicd-test",
        "product_id": "411968ab-9f17-40dd-8378-f22d8e39acbb",
        "offer_id": "2b89558b-8ed3-4d45-b79d-833bda781b7e",
        "config_yml": config_yml,
        "manifest_yml": manifest_yml,
    }
    setup_patched_app(monkeypatch, update_args)
    publish_args = {
        "command": "publish",
        "ama_name": "cicd-test",
        "product_id": "411968ab-9f17-40dd-8378-f22d8e39acbb",
        "offer_id": "2b89558b-8ed3-4d45-b79d-833bda781b7e",
        "config_yml": config_yml,
        "manifest_yml": manifest_yml,
    }
    setup_patched_app(monkeypatch, publish_args)
    ama_app.main()


def create_publish_publish_delete(config_yml, manifest_yml, monkeypatch):
    create_args = {"command": "create", "ama_name": "cicd-test", "config_yml": config_yml, "manifest_yml": manifest_yml}
    setup_patched_app(monkeypatch, create_args)
    product_id_json = json.loads(ama_app.main())
    assert product_id_json
    product_id = product_id_json["product_id"]
    offer_id = product_id_json["offer_id"]
    publish_args = {
        "command": "publish",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "offer_id": offer_id,
        "config_yml": config_yml,
        "manifest_yml": manifest_yml,
    }
    status_args = {
        "command": "status",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "config_yml": config_yml,
    }

    # Publish First Time
    setup_patched_app(monkeypatch, publish_args)
    ama_app.main()
    setup_patched_app(monkeypatch, status_args)
    status = ama_app.main()
    assert status

    # Publish Second Time
    setup_patched_app(monkeypatch, publish_args)
    ama_app.main()
    setup_patched_app(monkeypatch, status_args)
    status = ama_app.main()
    assert status

    delete_args = {"command": "delete", "product_id": product_id, "config_yml": config_yml}
    setup_patched_app(monkeypatch, delete_args)
    ama_app.main()


def status_check(config_yml, manifest_yml, monkeypatch):
    def mock_response_submissions_get(self, authorization, product_id):
        return namedtuple("response", ["value", "odata_etag", "id"])(*["", "", ""])

    monkeypatch.setattr(SubmissionApi, "products_product_id_submissions_get", mock_response_submissions_get)
    product_id = "test-id"

    status_args = {
        "command": "status",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "config_yml": config_yml,
    }
    setup_patched_app(monkeypatch, status_args)
    status = ama_app.main()
    assert status

    def mock_response_submissions_get(self, authorization, product_id):
        raise ApiException()

    monkeypatch.setattr(SubmissionApi, "products_product_id_submissions_get", mock_response_submissions_get)
    product_id = "test-id"

    status_args = {
        "command": "status",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "config_yml": config_yml,
    }
    setup_patched_app(monkeypatch, status_args)
    status = ama_app.main()
    assert status

    def mock_response_submissions_get(self, authorization, product_id):
        value = namedtuple("value", ["are_resources_ready", "state", "substate"])(*["true", "true", "true"])
        return namedtuple("response", ["value", "odata_etag", "id"])(*[[value], "", ""])

    monkeypatch.setattr(SubmissionApi, "products_product_id_submissions_get", mock_response_submissions_get)
    product_id = "test-id"

    status_args = {
        "command": "status",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "config_yml": config_yml,
    }
    setup_patched_app(monkeypatch, status_args)
    status = ama_app.main()
    assert status


def create_publish_missing_config(config_yml, manifest_yml, monkeypatch):
    publish_missing_config(config_yml, manifest_yml, monkeypatch)


def publish_missing_config(config_yml, manifest_yml, monkeypatch):
    create_args = {"command": "create", "ama_name": "cicd-test", "config_yml": config_yml, "manifest_yml": manifest_yml}
    setup_patched_app(monkeypatch, create_args)
    product_id_json = json.loads(ama_app.main())
    assert product_id_json
    product_id = product_id_json["product_id"]
    offer_id = product_id_json["offer_id"]
    publish_args = {
        "command": "publish",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "offer_id": offer_id,
        "config_yml": "not-config",
        "manifest_yml": manifest_yml,
    }
    setup_patched_app(monkeypatch, publish_args)
    with pytest.raises(FileNotFoundError):
        ama_app.main()
    delete_args = {"command": "delete", "product_id": product_id, "config_yml": config_yml}
    setup_patched_app(monkeypatch, delete_args)
    ama_app.main()


def create_publish_missing_manifest(config_yml, monkeypatch, manifest_yml):
    create_args = {"command": "create", "ama_name": "cicd-test", "config_yml": config_yml, "manifest_yml": manifest_yml}
    setup_patched_app(monkeypatch, create_args)
    product_id_json = json.loads(ama_app.main())
    assert product_id_json
    product_id = product_id_json["product_id"]
    publish_args = {
        "command": "publish",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "config_yml": config_yml,
        "manifest_yml": "not-found.yml",
    }
    setup_patched_app(monkeypatch, publish_args)
    with pytest.raises(FileNotFoundError):
        ama_app.main()
    delete_args = {"command": "delete", "product_id": product_id, "config_yml": config_yml}
    setup_patched_app(monkeypatch, delete_args)
    ama_app.main()


def get_status(config_yml, monkeypatch):
    product_id = "9e9a7597-63f8-4510-b4ab-4dd1fd85b211"
    status_args = {
        "command": "status",
        "ama_name": "cicd-test",
        "product_id": product_id,
        "config_yml": config_yml,
    }
    setup_patched_app(monkeypatch, status_args)
    status = ama_app.main()
    assert status


def setup_patched_app(monkeypatch, input_args):
    def get_args(self, args=None, namespace=None):
        return argparse.Namespace(**input_args)

    def get_known_args(self, args=None, namespace=None):
        return get_args(self, args=args, namespace=namespace), argparse.Namespace()

    monkeypatch.setattr(argparse.ArgumentParser, "parse_known_args", get_known_args)
    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", get_args)

    monkeypatch.setattr(sys, "argv", [""] + list(input_args.values()))
