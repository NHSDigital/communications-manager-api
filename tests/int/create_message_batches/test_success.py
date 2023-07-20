import requests
import pytest
import string
import random
import uuid
from lib import Assertions, Generators

VALID_ACCEPT_HEADERS = ["*/*", "application/json", "application/vnd.api+json"]
VALID_CONTENT_TYPE_HEADERS = ["application/json", "application/vnd.api+json"]
REQUEST_PATH = "/v1/message-batches"
VALID_DOB = ["0000-01-01", "2023-01-01", None]
valid_nhs_number = ''.join(random.choices(string.digits, k=10))


@pytest.mark.inttest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_accept_headers(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    data = Generators.generate_valid_create_message_batch_body(True)
    resp = requests.post(
      f"{nhsd_apim_proxy_url}{REQUEST_PATH}",
      headers={
          **nhsd_apim_auth_headers,
          "Accept": accept_headers,
          "Content-Type": "application/json"
      },
      json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_content_type_headers(nhsd_apim_proxy_url, nhsd_apim_auth_headers, content_type):
    data = Generators.generate_valid_create_message_batch_body(True)
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": content_type
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_nhs_number(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    data = Generators.generate_valid_create_message_batch_body(True)
    data["data"]["attributes"]["messages"][0]["recipient"]["nhsNumber"] = valid_nhs_number

    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
@pytest.mark.parametrize('dob', VALID_DOB)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers, dob):
    data = Generators.generate_valid_create_message_batch_body(True)
    data["data"]["attributes"]["messages"][0]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_without_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    data = Generators.generate_valid_create_message_batch_body(True)
    data["data"]["attributes"]["messages"][0]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])
