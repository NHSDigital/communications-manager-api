import requests
import pytest
from lib import Assertions, Permutations, Generators, Authentication
import lib.constants.constants as constants
from lib.constants.messages_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, MESSAGES_ENDPOINT

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.prodtest
def test_invalid_body():
    """
    .. include:: ../../partials/validation/test_messages_invalid.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        data="{}SF{}NOTVALID",
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_invalid_value_error("/"),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    MISSING_PROPERTIES_PATHS
)
def test_property_missing(property, pointer):
    """
    .. include:: ../../partials/validation/test_messages_property_missing.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_body("prod"),
            property
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_missing_value_error(pointer),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    NULL_PROPERTIES_PATHS
)
def test_data_null(property, pointer):
    """
    .. include:: ../../partials/validation/test_messages_null.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_body("prod"),
            property
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_null_value_error(pointer),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    INVALID_PROPERTIES_PATHS
)
def test_data_invalid(property, pointer):
    """
    .. include:: ../../partials/validation/test_messages_invalid.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            property,
            "invalid string"
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_invalid_value_error(pointer),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("nhs_number", constants.INVALID_NHS_NUMBER)
def test_invalid_nhs_number(nhs_number):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "nhsNumber",
            nhs_number
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_invalid_nhs_number_error("/data/attributes/recipient/nhsNumber"),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("dob", constants.INVALID_DOB)
def test_invalid_dob(dob):
    """
    .. include:: ../../partials/validation/test_invalid_dob.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "dateOfBirth",
            dob
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/recipient/dateOfBirth"),
        None
    )


@pytest.mark.prodtest
def test_invalid_routing_plan():
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "routingPlanId",
            "invalid"
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        None
    )


@pytest.mark.prodtest
def test_invalid_message_reference():
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "messageReference",
            "invalid"
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messageReference"),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", constants.INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "personalisation",
            personalisation
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/personalisation"),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", constants.NULL_VALUES)
def test_null_personalisation(personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "personalisation",
            personalisation
        ),
    )

    Assertions.assert_error_with_optional_None(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/personalisation"),
        None
    )
