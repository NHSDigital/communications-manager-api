import requests
import pytest
import time
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.fixtures import *


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
            "Authorization": bearer_token_int,
            "Accept": accept_headers,
            "Content-Type": "application/json",
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


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
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": content_type,
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.inttest
def test_201_message_batch_valid_nhs_number(bearer_token_int):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    resp = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.inttest
@pytest.mark.parametrize("dob", constants.VALID_DOB)
def test_201_message_batch_valid_dob(bearer_token_int, dob):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_valid_dob.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")
    data["data"]["attributes"]["messages"][0]["recipient"]["dateOfBirth"] = dob

    resp = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.inttest
def test_request_without_dob(bearer_token_int):
    """
    .. include:: ../../partials/happy_path/test_201_message_batch_without_dob.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")
    data["data"]["attributes"]["messages"][0]["recipient"].pop("dateOfBirth")

    resp = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=data,
    )
    Assertions.assert_201_response(
        resp,
        data["data"]["attributes"]["messageBatchReference"],
        data["data"]["attributes"]["routingPlanId"],
    )


@pytest.mark.inttest
def test_201_message_batches_request_idempotency(bearer_token_int):
    """
    .. include:: ../../partials/happy_path/test_201_message_batches_request_idempotency.rst
    """
    data = Generators.generate_valid_create_message_batch_body("int")

    respOne = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=data,
    )

    time.sleep(5)

    respTwo = requests.post(
        f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=data,
    )

    Assertions.assert_message_batches_idempotency(respOne, respTwo)
