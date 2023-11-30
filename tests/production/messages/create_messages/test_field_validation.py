import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators, Authentication
import lib.constants.constants as constants
from lib.constants.messages_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, MESSAGES_ENDPOINT

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_body(correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_body.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        data="{}SF{}NOTVALID",
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    MISSING_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_property_missing(property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_property_missing.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_body("prod"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_missing_value_error(pointer),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    NULL_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_null(property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_null.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_body("prod"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error(pointer),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    INVALID_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_invalid(property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_invalid.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            property,
            "invalid string"
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error(pointer),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("nhs_number", constants.INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_nhs_number(nhs_number, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "nhsNumber",
            nhs_number
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_nhs_number_error("/data/attributes/recipient/nhsNumber"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("dob", constants.INVALID_DOB)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_dob(dob, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_dob.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "dateOfBirth",
            dob
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/recipient/dateOfBirth"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_routing_plan(correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "routingPlanId",
            "invalid"
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_reference(correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "messageReference",
            "invalid"
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messageReference"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "personalisation",
            personalisation
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/personalisation"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.NULL_VALUES)
def test_null_personalisation(correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "personalisation",
            personalisation
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/messages/0/personalisation"),
        correlation_id
    )
