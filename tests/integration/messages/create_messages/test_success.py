import requests
import pytest
import time
from lib import Assertions, Generators, Authentication
from lib.constants.constants import INT_URL, VALID_CONTENT_TYPE_HEADERS, VALID_ACCEPT_HEADERS, \
    VALID_NHS_NUMBER, VALID_DOB, VALID_ROUTING_PLAN_ID_INT
from lib.constants.messages_paths import MESSAGES_ENDPOINT


@pytest.mark.inttest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
def test_201_message_batch_valid_accept_headers(accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    resp = requests.post(
        f"{INT_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
        json=data
    )
    Assertions.assert_201_response_messages(resp, "int")


@pytest.mark.inttest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
def test_201_message_batch_valid_content_type_headers(content_type):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": "application/json",
            "Content-Type": content_type
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, "int")


@pytest.mark.inttest
def test_201_message_batch_valid_nhs_number():
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = VALID_NHS_NUMBER

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, "int")


@pytest.mark.inttest
def test_201_try_different_app_id():
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = VALID_NHS_NUMBER

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": "application/json",
            "Content-Type": "application/json",
            "UseClient": "no_ods_override"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, "int")


@pytest.mark.inttest
@pytest.mark.parametrize('dob', VALID_DOB)
def test_201_message_batch_valid_dob(dob):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            "Authorization": Authentication.generate_authentication("int"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, "int")


@pytest.mark.inttest
def test_request_without_dob():
    """
    .. include:: ../../partials/happy_path/test_201_messages_without_dob.rst
    """
    data = Generators.generate_valid_create_message_body("int")
    data["data"]["attributes"]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, "int")


@pytest.mark.inttest
def test_201_message_request_idempotency():
    """
    .. include:: ../../partials/happy_path/test_201_messages_request_idempotency.rst
    """
    data = Generators.generate_valid_create_message_body("int")

    respOne = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )

    time.sleep(5)

    respTwo = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )

    Assertions.assert_messages_idempotency(respOne, respTwo)
