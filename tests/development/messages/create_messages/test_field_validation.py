import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators
from lib.fixtures import *  # NOSONAR
import lib.constants.constants as constants
from lib.constants.messages_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, MESSAGES_ENDPOINT


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_body(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_body.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        data="{}SF{}NOTVALID",
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize(
    "property, pointer",
    MISSING_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_property_missing(nhsd_apim_proxy_url, bearer_token_internal_dev, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_property_missing.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_missing_value_error(pointer),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize(
    "property, pointer",
    NULL_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_null(nhsd_apim_proxy_url, bearer_token_internal_dev, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_null.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error(pointer),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize(
    "property, pointer",
    INVALID_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_invalid(nhsd_apim_proxy_url, bearer_token_internal_dev, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_invalid.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("sandbox"),
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


@pytest.mark.devtest
@pytest.mark.parametrize("nhs_number", constants.INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_nhs_number(nhsd_apim_proxy_url, bearer_token_internal_dev, nhs_number, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["nhsNumber"] = nhs_number
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_nhs_number_error("/data/attributes/recipient/nhsNumber"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_routing_plan(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["routingPlanId"] = "invalid"
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_reference(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["messageReference"] = "invalid"
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messageReference"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["personalisation"] = personalisation
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/personalisation"),
        correlation_id
    )


@pytest.mark.devtest
def test_too_large_personalisation(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/validation/test_too_large_personalisation.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["routingPlanId"] = constants.GLOBAL_ROUTING_CONFIGURATION_SMS
    data["data"]["attributes"]["personalisation"] = {
        'sms_body': 'x'*919
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_personalisation_error(
            "Total personalisation length of 919 exceeding the maximum length of 918",
            "/data/attributes/personalisation"),
        None
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.NULL_VALUES)
def test_null_personalisation(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["personalisation"] = personalisation
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/personalisation"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_sms_contact_details(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_sms.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {"sms": "11111111111"}
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
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


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_email_contact_details(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_email.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {"email": "invalidEmailAddress"}
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
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


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_address_contact_details_too_few_lines(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_few.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1"],
            "postcode": "test"
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
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


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_address_contact_details_too_many_lines(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_many.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2", "3", "4", "5", "6"],
            "postcode": "test"
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
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


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_address_contact_details_postcode(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_postcode.rst
    """
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2", "3", "4", "5"],
            "postcode": "LS1 6AECD"
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
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
