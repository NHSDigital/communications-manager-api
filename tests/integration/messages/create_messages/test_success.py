import requests
import pytest
import time
from lib import Assertions, Generators
from lib.constants.constants import DEFAULT_CONTENT_TYPE, INT_URL, VALID_CONTENT_TYPE_HEADERS, VALID_ACCEPT_HEADERS, \
    VALID_NHS_NUMBER, VALID_SMS_NUMBERS
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.fixtures import *  # NOSONAR


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
            "Authorization": bearer_token_int.value,
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
            "Authorization": bearer_token_int.value,
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
            "Authorization": bearer_token_int.value,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, INT_URL)


@pytest.mark.inttest
@pytest.mark.parametrize('valid_sms_numbers', VALID_SMS_NUMBERS)
def test_201_message_valid_contact_details(bearer_token_int, valid_sms_numbers):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_contact_details.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = VALID_NHS_NUMBER
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "sms": valid_sms_numbers,
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_int.value,
            "Accept": DEFAULT_CONTENT_TYPE,
            "Content-Type": DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, INT_URL)
