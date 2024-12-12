import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators
from lib.fixtures import *  # NOSONAR
import lib.constants.constants as constants
from lib.constants.shared_paths import ROUTING_PLAN_ID_PATH
from lib.constants.message_batches_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, DUPLICATE_PROPERTIES_PATHS, TOO_FEW_PROPERTIES_PATHS, MESSAGE_BATCH_REFERENCE_PATH, \
    FIRST_MESSAGE_RECIPIENT_NHSNUMBER_PATH, FIRST_MESSAGE_REFERENCE_PATH, MESSAGE_BATCHES_ENDPOINT

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
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
    .. include:: ../../partials/validation/test_message_batch_property_missing.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_batch_body("dev"),
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
    .. include:: ../../partials/validation/test_message_batch_null.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_batch_body("dev"),
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
    .. include:: ../../partials/validation/test_message_batch_invalid.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
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
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize(
    "property, pointer",
    DUPLICATE_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_duplicate(nhsd_apim_proxy_url, bearer_token_internal_dev, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_duplicate.rst
    """
    # Add a duplicate message to the payload to trigger the duplicate error
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_duplicate_value_error(pointer),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize(
    "property, pointer",
    TOO_FEW_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_too_few_items(nhsd_apim_proxy_url, bearer_token_internal_dev, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_too_few_items.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_internal_dev.value,
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("dev"),
            property,
            []
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_too_few_items_error(pointer),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("nhs_number", constants.INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_nhs_number(nhsd_apim_proxy_url, bearer_token_internal_dev, nhs_number, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["nhsNumber"] = nhs_number
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_invalid_nhs_number_error(FIRST_MESSAGE_RECIPIENT_NHSNUMBER_PATH),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_routing_plan(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["routingPlanId"] = "invalid"
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_invalid_value_error(ROUTING_PLAN_ID_PATH),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_batch_reference(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_batch_reference.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messageBatchReference"] = "invalid"
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_invalid_value_error(MESSAGE_BATCH_REFERENCE_PATH),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_reference(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["messageReference"] = "invalid"
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_invalid_value_error(FIRST_MESSAGE_REFERENCE_PATH),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("invalid_value", constants.INVALID_MESSAGE_VALUES)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_blank_value_under_messages(nhsd_apim_proxy_url, bearer_token_internal_dev, invalid_value, correlation_id):
    """
    .. include:: ../../partials/validation/test_blank_value_under_messages.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"] = [invalid_value]
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_invalid_value_error("/data/attributes/messages/0"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_null_value_under_messages(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_null_value_under_messages.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"] = [None]
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_null_value_error("/data/attributes/messages/0"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["personalisation"] = personalisation
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_invalid_value_error("/data/attributes/messages/0/personalisation"),
        correlation_id
    )


@pytest.mark.devtest
def test_too_large_personalisation(nhsd_apim_proxy_url, bearer_token_internal_dev):
    """
    .. include:: ../../partials/validation/test_too_large_personalisation.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["routingPlanId"] = constants.GLOBAL_ROUTING_CONFIGURATION_SMS
    data["data"]["attributes"]["messages"][0]["personalisation"] = {
        'sms_body': 'x'*919
    }
    while len(data["data"]["attributes"]["messages"]) > 1:
        del data["data"]["attributes"]["messages"][1]
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
            "/data/attributes/messages/0/personalisation"),
        None
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.NULL_VALUES)
def test_null_personalisation(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["personalisation"] = personalisation
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
        Generators.generate_null_value_error("/data/attributes/messages/0/personalisation"),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_sms_contact_details(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_sms.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {"sms": "077009000021"}
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
            "/data/attributes/messages/0/recipient/contactDetails/sms",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_sms_contact_details_second_message(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_sms.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": bearer_token_internal_dev.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609"
                        },
                        "personalisation": {}
                    },
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1c",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "contactDetails": {
                                "sms": "077009000021"
                            }
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/1/recipient/contactDetails/sms",
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
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {"email": "invalidEmailAddress"}
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
            "/data/attributes/messages/0/recipient/contactDetails/email",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_email_contact_details_third_message(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_email.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": bearer_token_internal_dev.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609"
                        },
                        "personalisation": {}
                    },
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1c",
                        "recipient": {
                            "nhsNumber": "9990548609"
                        },
                        "personalisation": {}
                    },
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1d",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "contactDetails": {
                                "email": "invalidEmailAddress"
                            }
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/2/recipient/contactDetails/email",
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
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1"],
            "postcode": "LS1 6AE"
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
            "/data/attributes/messages/0/recipient/contactDetails/address",
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
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2", "3", "4", "5", "6"],
            "postcode": "LS1 6AE"
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
            "/data/attributes/messages/0/recipient/contactDetails/address",
            "Invalid"
        ),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_address_contact_details_postcode(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_postcode.rst
    """
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2", "3", "4", "5"],
            "postcode": "LS1 6AECD"
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
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
            "/data/attributes/messages/0/recipient/contactDetails/address",
            "Postcode input failed format check"
        ),
        correlation_id
    )
