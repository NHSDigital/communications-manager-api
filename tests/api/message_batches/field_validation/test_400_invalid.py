import requests
import pytest
from lib import Assertions, Generators, Permutations
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import INVALID_NHS_NUMBER, INVALID_MESSAGE_VALUES, INVALID_PERSONALISATION_VALUES
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT, \
    INVALID_PROPERTIES_PATHS, FIRST_MESSAGE_RECIPIENT_NHSNUMBER_PATH, \
    ROUTING_PLAN_ID_PATH, MESSAGE_BATCH_REFERENCE_PATH, FIRST_MESSAGE_REFERENCE_PATH


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
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
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
@pytest.mark.parametrize("property, pointer", INVALID_PROPERTIES_PATHS)
def test_data_invalid(url, bearer_token, property, pointer):
    """
    .. include:: ../partials/validation/test_message_batch_invalid.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("dev"),
            property,
            "invalid string"
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error(pointer),
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
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["nhsNumber"] = nhs_number

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_nhs_number_error(FIRST_MESSAGE_RECIPIENT_NHSNUMBER_PATH),
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

    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["routingPlanId"] = "invalid"

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error(ROUTING_PLAN_ID_PATH),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_message_batch_reference(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_message_batch_reference.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messageBatchReference"] = "invalid"

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error(MESSAGE_BATCH_REFERENCE_PATH),
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
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["messageReference"] = ["invalid"]

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error(FIRST_MESSAGE_REFERENCE_PATH),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("invalid_value", INVALID_MESSAGE_VALUES)
def test_invalid_value_under_messages(url, bearer_token, invalid_value):
    """
    .. include:: ../partials/validation/test_invalid_value_under_messages.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"] = [invalid_value]

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messages/0"),
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
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["personalisation"] = personalisation

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messages/0/personalisation"),
        None
    )
