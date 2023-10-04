import requests
import pytest
from lib import Assertions, Generators

DEFAULT_CONTENT_TYPE = "application/json"
VALID_ACCEPT_HEADERS = ["*/*", DEFAULT_CONTENT_TYPE, "application/vnd.api+json"]
VALID_CONTENT_TYPE_HEADERS = [DEFAULT_CONTENT_TYPE, "application/vnd.api+json"]
REQUEST_PATH = "/v1/message-batches"
VALID_DOB = ["0000-01-01", "2023-01-01", None]
valid_nhs_number = "9990548609"


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_accept_headers(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    """
    .. py:function:: Scenario: An API consumer creating a batch of messages with a \
        valid accept header receives a 201 response

        | **Given** the API consumer provides a valid accept header when creating a batch of messages
        | **When** the request is submitted
        | **Then** the response is a 201 success

    **Asserts**
    - Response returns a 201 status code
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    resp = requests.post(
      f"{nhsd_apim_proxy_url}{REQUEST_PATH}",
      headers={
          **nhsd_apim_auth_headers,
          "Accept": accept_headers,
          "Content-Type": DEFAULT_CONTENT_TYPE
      },
      json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.devtest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_content_type_headers(nhsd_apim_proxy_url, nhsd_apim_auth_headers, content_type):
    """
    .. py:function:: Scenario: An API consumer creating a batch of messages with a \
        valid content type header receives a 201 response

        | **Given** the API consumer provides a valid content type header when creating a batch of messages
        | **When** the request is submitted
        | **Then** the response is a 201 success

    **Asserts**
    - Response returns a 201 status code
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": DEFAULT_CONTENT_TYPE,
            "Content-Type": content_type
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_nhs_number(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. py:function:: Scenario: An API consumer creating a batch of messages with a \
        valid NHS number receives a 201 response

        | **Given** the API consumer provides a valid NHS number for a recipient in their new message batch
        | **When** the request is submitted
        | **Then** the response is a 201 success

    **Asserts**
    - Response returns a 201 status code
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["nhsNumber"] = valid_nhs_number

    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": DEFAULT_CONTENT_TYPE,
            "Content-Type": DEFAULT_CONTENT_TYPE
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.devtest
@pytest.mark.parametrize('dob', VALID_DOB)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers, dob):
    """
    .. py:function:: Scenario: An API consumer creating a batch of messages with a \
        valid date of birth receives a 201 response

        | **Given** the API consumer provides a valid date of birth for a recipient in their new message batch
        | **When** the request is submitted
        | **Then** the response is a 201 success

    **Asserts**
    - Response returns a 201 status code
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": DEFAULT_CONTENT_TYPE,
            "Content-Type": DEFAULT_CONTENT_TYPE
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_without_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. py:function:: Scenario: An API consumer creating a batch of messages with a \
        date of birth receives a 201 response

        | **Given** the API consumer does not provide a date of birth for a recipient in their new message batch
        | **When** the request is submitted
        | **Then** the response is a 201 success

    **Asserts**
    - Response returns a 201 status code
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
        **nhsd_apim_auth_headers,
        "Accept": DEFAULT_CONTENT_TYPE,
        "Content-Type": DEFAULT_CONTENT_TYPE
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])
