import requests
import pytest
import time
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
import lib.constants.constants as constants


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_201_message_valid_accept_headers(nhsd_apim_proxy_url, bearer_token_internal_dev, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": accept_headers,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
@pytest.mark.parametrize('content_type', constants.VALID_CONTENT_TYPE_HEADERS)
def test_201_message_valid_content_type_headers(nhsd_apim_proxy_url, bearer_token_internal_dev, content_type):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": content_type
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
def test_201_message_valid_nhs_number(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = constants.VALID_NHS_NUMBER

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
def test_201_message_valid_contact_details(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_contact_details.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = constants.VALID_NHS_NUMBER
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "sms": "07777777777",
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
@pytest.mark.parametrize('dob', constants.VALID_DOB)
def test_201_message_valid_dob(nhsd_apim_proxy_url, bearer_token_internal_dev, dob):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
def test_request_without_dob(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_201_messages_without_dob.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
def test_201_message_request_idempotency(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/happy_path/test_201_messages_request_idempotency.rst
    """
    data = Generators.generate_valid_create_message_body("dev")

    resp_one = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    time.sleep(5)

    resp_two = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_messages_idempotency(resp_one, resp_two)
