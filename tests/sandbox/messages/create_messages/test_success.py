import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.messages_paths import MESSAGES_ENDPOINT

VALID_ROUTING_PLAN_ID_AND_VERSION = [
    ("b838b13c-f98c-4def-93f0-515d4e4f4ee1", "ztoe2qRAM8M8vS0bqajhyEBcvXacrGPp"),
    ("49e43b98-70cb-47a9-a55e-fe70c9a6f77c", "G.uwELAFAGMsKEBk2iIeRCBOB6kj6OkE"),
    ("b402cd20-b62a-4357-8e02-2952959531c8", "J7ZPQIf1yyUB4CiBpUBoy.1ahfOTCCQ7"),
    ("936e9d45-15de-4a95-bb36-ae163c33ae53", "riOAKoN4ajoVyUf9U2xwHVNRHc5V52A."),
    ("9ba00d23-cd6f-4aca-8688-00abc85a7980", "nkz2osS_oc8IZ5GqeN_1yXKSXe9VEUjV"),
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', constants.VALID_ACCEPT_HEADERS)
def test_201_single_message_with_valid_accept_headers(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Accept": accept_headers,
            "Content-Type": "application/json"
        },
        json=data
    )
    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type', constants.VALID_CONTENT_TYPE_HEADERS)
def test_201_single_message_with_valid_content_type_headers(nhsd_apim_proxy_url, content_type):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Accept": "application/json",
            "Content-Type": content_type
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.sandboxtest
def test_201_single_message_with_valid_nhs_number(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = constants.VALID_NHS_NUMBER

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.sandboxtest
def test_201_single_message_with_valid_contact_details(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_contact_details.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
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
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('dob', constants.VALID_DOB)
def test_201_single_message_with_valid_dob(nhsd_apim_proxy_url, dob):
    """
    .. include:: ../../partials/happy_path/test_201_messages_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    data["data"]["attributes"]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)


@pytest.mark.sandboxtest
def test_single_message_with_without_dob(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/happy_path/test_201_messages_without_dob.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    data["data"]["attributes"]["recipient"].pop("dateOfBirth")

    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response_messages(resp, nhsd_apim_proxy_url)
