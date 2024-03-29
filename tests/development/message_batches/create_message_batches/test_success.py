import requests
import pytest
import time
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.devtest
@pytest.mark.parametrize("accept_headers", constants.VALID_ACCEPT_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_accept_headers(
    nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers
):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_accept_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **nhsd_apim_auth_headers,
            "Accept": accept_headers,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.devtest
@pytest.mark.parametrize("content_type", constants.VALID_CONTENT_TYPE_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_content_type_headers(
    nhsd_apim_proxy_url, nhsd_apim_auth_headers, content_type
):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_content_type_headers.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": content_type,
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_nhs_number(
    nhsd_apim_proxy_url, nhsd_apim_auth_headers
):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"][
        "nhsNumber"
    ] = constants.VALID_NHS_NUMBER

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.devtest
@pytest.mark.parametrize("dob", constants.VALID_DOB)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers, dob):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_without_dob(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_without_dob.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"].pop("dateOfBirth")

    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batches_request_idempotency(
    nhsd_apim_proxy_url, nhsd_apim_auth_headers
):
    """
    .. include:: ../../partials/happy_path/test_201_message_batches_request_idempotency.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")

    respOne = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )

    time.sleep(5)

    respTwo = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **nhsd_apim_auth_headers,
            "Accept": constants.DEFAULT_CONTENT_TYPE,
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        },
        json=data,
    )

    Assertions.assert_message_batches_idempotency(respOne, respTwo)
