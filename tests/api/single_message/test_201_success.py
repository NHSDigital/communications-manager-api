import requests
import pytest
from lib import Assertions, Helper, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.constants import VALID_ACCEPT_HEADERS, DEFAULT_CONTENT_TYPE, \
    VALID_CONTENT_TYPE_HEADERS, VALID_NHS_NUMBER, VALID_SMS_NUMBERS


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
def test_201_message_valid_accept_headers(url, bearer_token, accept_headers):
    """
    .. include:: /partials/happy_path/test_201_messages_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_body("dev")

    resp = requests.post(f"{url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token.value,
            "Accept": accept_headers,
            "Content-Type": DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, url)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
def test_201_message_valid_content_type_headers(url, bearer_token, content_type):
    """
    .. include:: /partials/happy_path/test_201_messages_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    resp = requests.post(f"{url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token.value,
            "Accept": DEFAULT_CONTENT_TYPE,
            "Content-Type": content_type
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, url)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
def test_201_message_valid_nhs_number(url, bearer_token):
    """
    .. include:: /partials/happy_path/test_201_messages_valid_nhs_number.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = VALID_NHS_NUMBER

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_201_response_messages(resp, url)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
def test_201_message_undefined_nhs_number(url, bearer_token):
    """
    .. include:: /partials/happy_path/test_201_messages_undefined_nhs_number.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"].pop("nhsNumber", None)

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_201_response_messages(resp, url)


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.parametrize('valid_sms_numbers', VALID_SMS_NUMBERS)
def test_201_message_valid_contact_details(url, bearer_token, valid_sms_numbers):
    """
    .. include:: ../partials/happy_path/test_201_messages_valid_contact_details.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = VALID_NHS_NUMBER
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "sms": valid_sms_numbers,
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_201_response_messages(resp, url)


@pytest.mark.test
@pytest.mark.devtest
def test_201_message_terminal_failed_status(url, bearer_token):
    """
    .. include:: ../partials/happy_path/test_201_messages_terminal_failed_status.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"].pop("nhsNumber", None)
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "name": {
            "firstName": "name",
            "lastName": "last"
        }
    }

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_201_response_messages(resp, url)

    message_id = resp.json().get("data").get("id")

    Helper.poll_get_message(url=url, headers=headers, message_id=message_id, end_state="failed")

    resp = Helper.get_message(url, headers, message_id)

    Assertions.assert_get_message_status(
        resp,
        "failed",
        "Failed reason: No valid request item plans were generated",
        "MFR_CFGV_0005"
    )

    Assertions.assert_get_message_response_channels(
        resp,
        "failed",
        "Failed reason: Not registered with NHS App",
        "CFR_SUPE_0001"
    )
