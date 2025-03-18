import requests
import pytest
import time
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.fixtures import *  # NOSONAR


@pytest.mark.inttest
@pytest.mark.parametrize("accept_headers", constants.VALID_ACCEPT_HEADERS)
def test_201_message_batch_valid_accept_headers(bearer_token_int, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    resp = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
            "Accept": accept_headers,
            "Content-Type": "application/json",
        },
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.inttest
@pytest.mark.parametrize("content_type", constants.VALID_CONTENT_TYPE_HEADERS)
def test_201_message_batch_valid_content_type_headers(bearer_token_int, content_type):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    resp = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
            "Accept": "application/json",
            "Content-Type": content_type,
        },
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.inttest
def test_201_message_batch_valid_nhs_number(bearer_token_int):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    resp = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.inttest
@pytest.mark.parametrize('valid_sms_numbers', constants.VALID_SMS_NUMBERS)
def test_201_message_batch_valid_contact_details(
    bearer_token_int,
    valid_sms_numbers
):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_contact_details.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")
    data["data"]["attributes"]["messages"][0]["recipient"][
        "nhsNumber"
    ] = constants.VALID_NHS_NUMBER
    data["data"]["attributes"]["messages"][0]["recipient"][
        "contactDetails"
    ] = {
        "sms": valid_sms_numbers,
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }

    resp = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )
    Assertions.assert_201_response(resp, data)
