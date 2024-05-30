import requests
import pytest
import time
from lib import Assertions, Generators
from lib.constants.constants import INT_URL, VALID_CONTENT_TYPE_HEADERS, VALID_ACCEPT_HEADERS, \
    VALID_NHS_NUMBER, VALID_DOB, VALID_ROUTING_PLAN_ID_INT
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.fixtures import *


@pytest.mark.inttest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
def test_201_single_message_with_valid_accept_headers(bearer_token_int, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    resp = requests.post(
        f"{INT_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int,
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
        json=data
    )
    Assertions.assert_201_response_messages(resp, INT_URL)


@pytest.mark.inttest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
def test_201_single_message_with_valid_content_type_headers(bearer_token_int, content_type):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": content_type
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, INT_URL)


@pytest.mark.inttest
def test_201_single_message_with_valid_nhs_number(bearer_token_int):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = VALID_NHS_NUMBER

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, INT_URL)


@pytest.mark.inttest
@pytest.mark.parametrize('dob', VALID_DOB)
def test_201_single_message_with_valid_dob(bearer_token_int, dob):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, INT_URL)


@pytest.mark.inttest
def test_single_message_request_without_dob(bearer_token_int):
    """
    .. include:: ../../partials/happy_path/test_201_messages_without_dob.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, INT_URL)


@pytest.mark.inttest
def test_201_message_request_idempotency(bearer_token_int):
    """
    .. include:: ../../partials/happy_path/test_201_messages_request_idempotency.rst
    """
    data = Generators.generate_valid_create_message_body("int")

    respOne = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )

    time.sleep(5)

    respTwo = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )

    Assertions.assert_messages_idempotency(respOne, respTwo)
