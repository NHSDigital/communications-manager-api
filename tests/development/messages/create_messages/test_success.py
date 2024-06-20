import requests
import pytest
import time
from lib import Assertions, Generators, Authentication
from lib.constants.messages_paths import MESSAGES_ENDPOINT
import lib.constants.constants as constants


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_201_message_valid_accept_headers(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": accept_headers,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
@pytest.mark.parametrize('content_type', constants.VALID_CONTENT_TYPE_HEADERS)
def test_201_message_valid_content_type_headers(nhsd_apim_proxy_url, content_type):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": content_type
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
def test_201_message_valid_nhs_number(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = constants.VALID_NHS_NUMBER

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
@pytest.mark.parametrize('dob', constants.VALID_DOB)
def test_201_message_valid_dob(nhsd_apim_proxy_url, dob):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
def test_request_without_dob(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/happy_path/test_201_messages_without_dob.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.devtest
def test_201_message_request_idempotency(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/happy_path/test_201_messages_request_idempotency.rst
    """
    data = Generators.generate_valid_create_message_body("dev")

    respOne = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    time.sleep(5)

    respTwo = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("internal-dev"),
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_messages_idempotency(respOne, respTwo)
