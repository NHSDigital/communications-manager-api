import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants import *

VALID_ACCEPT_HEADERS = ["*/*", "application/json", "application/vnd.api+json"]
VALID_CONTENT_TYPE_HEADERS = ["application/json", "application/vnd.api+json"]
REQUEST_PATH = "/v1/message-batches"
VALID_DOB = ["0000-01-01", "2023-01-01", None]
valid_nhs_number = "9990548609"


@pytest.mark.inttest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
def test_201_message_batch_valid_accept_headers(accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    resp = requests.post(
      f"{INT_URL}{REQUEST_PATH}",
      headers={
          "Authorization": Authentication.generate_authentication("int"),
          "Accept": accept_headers,
          "Content-Type": "application/json"
      },
      json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
def test_201_message_batch_valid_content_type_headers(content_type):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    resp = requests.post(f"{INT_URL}{REQUEST_PATH}", headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": "application/json",
            "Content-Type": content_type
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
def test_201_message_batch_valid_nhs_number():
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    resp = requests.post(f"{INT_URL}{REQUEST_PATH}", headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
@pytest.mark.parametrize('dob', VALID_DOB)
def test_201_message_batch_valid_dob(dob):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")
    data["data"]["attributes"]["messages"][0]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{INT_URL}{REQUEST_PATH}", headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.inttest
def test_request_without_dob():
    """
    .. include:: ../../partials/happy_path/test_request_without_dob.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")
    data["data"]["attributes"]["messages"][0]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{INT_URL}{REQUEST_PATH}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])
