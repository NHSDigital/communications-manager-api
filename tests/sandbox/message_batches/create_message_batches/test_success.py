import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT

VALID_ROUTING_PLAN_ID = [
    "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
    "49e43b98-70cb-47a9-a55e-fe70c9a6f77c",
    "b402cd20-b62a-4357-8e02-2952959531c8",
    "936e9d45-15de-4a95-bb36-ae163c33ae53",
    "9ba00d23-cd6f-4aca-8688-00abc85a7980",
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("accept_headers", constants.VALID_ACCEPT_HEADERS)
def test_201_message_batch_valid_accept_headers(nhsd_apim_proxy_url, accept_headers):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={"Accept": accept_headers, "Content-Type": "application/json"},
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.sandboxtest
@pytest.mark.parametrize("content_type", constants.VALID_CONTENT_TYPE_HEADERS)
def test_201_message_batch_valid_content_type_headers(
    nhsd_apim_proxy_url, content_type
):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={"Accept": "application/json", "Content-Type": content_type},
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.sandboxtest
@pytest.mark.parametrize("routing_plan_id", VALID_ROUTING_PLAN_ID)
def test_201_message_batch_valid_routing_plan_id(nhsd_apim_proxy_url, routing_plan_id):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_routing_plan_id.rst
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")
    data["data"]["attributes"]["routingPlanId"] = routing_plan_id

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.sandboxtest
def test_201_message_batch_valid_nhs_number(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")
    data["data"]["attributes"]["messages"][0]["recipient"][
        "nhsNumber"
    ] = constants.VALID_NHS_NUMBER

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json=data,
    )
    Assertions.assert_201_response(resp, data)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('valid_sms_numbers', constants.VALID_SMS_NUMBERS)
def test_201_message_batch_valid_contact_details(nhsd_apim_proxy_url, valid_sms_numbers):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_contact_details.rst
    """
    data = Generators.generate_valid_create_message_batch_body("sandbox")
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
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json=data,
    )
    Assertions.assert_201_response(resp, data)
