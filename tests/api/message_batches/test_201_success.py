import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import VALID_ACCEPT_HEADERS, DEFAULT_CONTENT_TYPE, \
    VALID_CONTENT_TYPE_HEADERS, VALID_NHS_NUMBER
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.parametrize("accept_headers", VALID_ACCEPT_HEADERS)
def test_201_message_batch_valid_accept_headers(url, bearer_token, accept_headers):
    """
    .. include:: ../partials/happy_path/test_201_message_batch_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token.value,
            "Accept": accept_headers,
            "Content-Type": DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.parametrize("content_type", VALID_CONTENT_TYPE_HEADERS)
def test_201_message_batch_valid_content_type_headers(url, bearer_token, content_type):
    """
    .. include:: ../partials/happy_path/test_201_message_batch_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token.value,
            "Accept": DEFAULT_CONTENT_TYPE,
            "Content-Type": content_type,
        },
        json=data,
    )

    Assertions.assert_201_response(resp, data)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
def test_201_message_batch_valid_nhs_number(url, bearer_token):
    """
    .. include:: ../partials/happy_path/test_201_message_batch_valid_nhs_number.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["nhsNumber"] = VALID_NHS_NUMBER

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data,
    )

    Assertions.assert_201_response(resp, data)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
def test_201_message_batch_undefined_nhs_number(url, bearer_token):
    """
    .. include:: ../partials/happy_path/test_201_message_batch_undefined_nhs_number.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"].pop("nhsNumber", None)

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
def test_201_message_batch_valid_contact_details(url, bearer_token):
    """
    .. include:: ../partials/happy_path/test_201_message_batch_valid_contact_details.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "sms": "07777777777",
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data,
    )
    Assertions.assert_201_response(resp, data)
