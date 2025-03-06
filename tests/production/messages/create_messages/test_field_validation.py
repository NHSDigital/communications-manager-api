import requests
import pytest
from lib import Assertions, Permutations, Generators
import lib.constants.constants as constants
from lib.constants.messages_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, MESSAGES_ENDPOINT
from lib.fixtures import *  # NOSONAR

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.prodtest
def test_invalid_body(bearer_token_prod):
    """
    .. include:: ../../partials/validation/test_messages_invalid.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
        },
        data="{}SF{}NOTVALID",
    )

    Assertions.assert_error_with_optional_correlation_id(
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
def test_property_missing(bearer_token_prod, property, pointer):
    """
    .. include:: ../../partials/validation/test_messages_property_missing.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    NULL_PROPERTIES_PATHS
)
def test_data_null(bearer_token_prod, property, pointer):
    """
    .. include:: ../../partials/validation/test_messages_null.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    INVALID_PROPERTIES_PATHS
)
def test_data_invalid(bearer_token_prod, property, pointer):
    """
    .. include:: ../../partials/validation/test_messages_invalid.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("nhs_number", constants.INVALID_NHS_NUMBER)
def test_invalid_nhs_number(bearer_token_prod, nhs_number):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
def test_invalid_routing_plan(bearer_token_prod):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
def test_invalid_message_reference(bearer_token_prod):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", constants.INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(bearer_token_prod, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", constants.NULL_VALUES)
def test_null_personalisation(bearer_token_prod, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        Generators.generate_null_value_error("/data/attributes/personalisation"),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_sms_contact_details(bearer_token_prod, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_sms.rst
    """
    data = Generators.generate_valid_create_message_body("prod")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {"sms": "11111111111"}
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_prod.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/sms",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_email_contact_details(bearer_token_prod, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_email.rst
    """
    data = Generators.generate_valid_create_message_body("prod")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {"email": "invalidEmailAddress"}
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_prod.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/email",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_address_contact_details_too_few_lines(bearer_token_prod, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_few.rst
    """
    data = Generators.generate_valid_create_message_body("prod")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1"],
            "postcode": "test"
        }
    }
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_prod.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_too_few_items_error_custom_detail(
            "/data/attributes/recipient/contactDetails/address",
            "Too few address lines were provided"
        ),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_address_contact_details_too_many_lines(bearer_token_prod, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_many.rst
    """
    data = Generators.generate_valid_create_message_body("prod")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2", "3", "4", "5", "6"],
            "postcode": "test"
        }
    }
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_prod.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/address",
            "Too many address lines were provided"
        ),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_address_contact_details_postcode(bearer_token_prod, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_postcode.rst
    """
    data = Generators.generate_valid_create_message_body("prod")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2", "3", "4", "5"],
            "postcode": "LS1 6AECD"
        }
    }
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_prod.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/address",
            "Postcode input failed format check"
        ),
        correlation_id
    )
