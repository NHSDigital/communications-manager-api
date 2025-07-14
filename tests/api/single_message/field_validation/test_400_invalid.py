import requests
import pytest
from lib import Assertions, Permutations, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import INVALID_PROPERTIES_PATHS, MESSAGES_ENDPOINT
from lib.constants.constants import INVALID_NHS_NUMBER, INVALID_PERSONALISATION_VALUES


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_body(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_body.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        data="{}SF{}NOTVALID",
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/"),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("nhs_number", INVALID_NHS_NUMBER)
def test_invalid_nhs_number(url, bearer_token, nhs_number):
    """
    .. include:: ../partials/validation/test_invalid_nhs_number.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = nhs_number

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_nhs_number_error("/data/attributes/recipient/nhsNumber"),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_routing_plan(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_routing_plan.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["routingPlanId"] = "invalid"

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_message_reference(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_message_reference.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["messageReference"] = 90

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messageReference"),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(url, bearer_token, personalisation):
    """
    .. include:: ../partials/validation/test_invalid_personalisation.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["personalisation"] = personalisation

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/personalisation"),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_recipient(url, bearer_token):
    """
    .. include:: ../partials/validation/test_messages_invalid.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"] = "invalid"

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/recipient"),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_data_type(url, bearer_token):
    """
    .. include:: ../partials/validation/test_messages_invalid.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["type"] = "invalid"

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/type"),
        None
    )
