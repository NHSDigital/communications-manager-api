import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT
import lib.constants.constants as constants

CORRELATION_ID = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
DUPLICATE_ROUTING_PLAN_TEMPLATE_ID = "bb454d66-033b-45c0-bbb6-d9b3420a0bd4"


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_valid_accept_headers(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    # """
    # .. include:: ../../partials/happy_path/test_201.rst
    # """
    data = Generators.generate_valid_create_message_body("dev")
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            **nhsd_apim_auth_headers,
            "Accept": accept_headers,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, "internal-dev")


@pytest.mark.devtest
@pytest.mark.parametrize('content_type', constants.VALID_CONTENT_TYPE_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_valid_content_type_headers(nhsd_apim_proxy_url, nhsd_apim_auth_headers, content_type):
    # """
    # .. include:: ../../partials/happy_path/test_201.rst
    # """
    data = Generators.generate_valid_create_message_body("dev")
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": content_type
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, "internal-dev")


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_valid_nhs_number(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    # """
    # .. include:: ../../partials/happy_path/test_201.rst
    # """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = constants.VALID_NHS_NUMBER

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, "internal-dev")


@pytest.mark.devtest
@pytest.mark.parametrize('dob', constants.VALID_DOB)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers, dob):
    # """
    # .. include:: ../../partials/happy_path/test_201.rst
    # """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, "internal-dev")


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_without_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    # """
    # .. include:: ../../partials/happy_path/test_201.rst
    # """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE
        }, json=data
    )

    Assertions.assert_201_response_messages(resp, "internal-dev")
