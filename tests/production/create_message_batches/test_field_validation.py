import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators, Authentication
import lib.constants.constants as constants
from lib.constants.message_batches_paths import *

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
INVALID_MESSAGE_VALUES = ["", [], 5, 0.1]
INVALID_NHS_NUMBER = ["012345678", "01234567890", "abcdefghij", "", [], {}, 5, 0.1]
INVALID_DOB = ["1990-10-1", "1990-1-10", "90-10-10", "10-12-1990", "1-MAY-2000", "1990/01/01", "", [], {}, 5, 0.1]


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_body(correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_body.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}/v1/message-batches",
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
    .. include:: ../../partials/validation/test_property_missing.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_batch_body(),
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
    .. include:: ../../partials/validation/test_data_null.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_batch_body(),
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
    .. include:: ../../partials/validation/test_data_invalid.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body(),
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
@pytest.mark.parametrize(
    "property, pointer",
    DUPLICATE_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_duplicate(property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_duplicate.rst
    """
    # Add a duplicate message to the payload to trigger the duplicate error
    data = Generators.generate_valid_create_message_batch_body()
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{constants.PROD_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_duplicate_value_error(pointer),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    TOO_FEW_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_too_few_items(property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_too_few_items.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body(),
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


@pytest.mark.prodtest
@pytest.mark.parametrize("nhs_number", INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_nhs_number(nhs_number, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(f"{constants.PROD_URL}/v1/message-batches", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}"
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": nhs_number,
                            "dateOfBirth": "1982-1-11"
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
        Generators.generate_invalid_nhs_number_error("/data/attributes/messages/0/recipient/nhsNumber"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("dob", INVALID_DOB)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_dob(dob, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_dob.rst
    """
    resp = requests.post(f"{constants.PROD_URL}/v1/message-batches", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}"
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": dob
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
        Generators.generate_invalid_value_error("/data/attributes/messages/0/recipient/dateOfBirth"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_routing_plan(correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(f"{constants.PROD_URL}/v1/message-batches", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}"
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "invalid",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2000-01-01"
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
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_batch_reference(correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_batch_reference.rst
    """
    resp = requests.post(f"{constants.PROD_URL}/v1/message-batches", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}"
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": "invalid",
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2000-01-01"
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
        Generators.generate_invalid_value_error("/data/attributes/messageBatchReference"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_reference(correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(f"{constants.PROD_URL}/v1/message-batches", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}"
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "invalid",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2000-01-01"
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
        Generators.generate_invalid_value_error("/data/attributes/messages/0/messageReference"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("invalid_value", INVALID_MESSAGE_VALUES)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_blank_value_under_messages(invalid_value, correlation_id):
    """
    .. include:: ../../partials/validation/test_blank_value_under_messages.rst
    """
    resp = requests.post(f"{constants.PROD_URL}/v1/message-batches", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}"
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    invalid_value
                ],
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messages/0"),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_null_value_under_messages(correlation_id):
    """
    .. include:: ../../partials/validation/test_null_value_under_messages.rst
    """
    resp = requests.post(f"{constants.PROD_URL}/v1/message-batches", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": f"{Authentication.generate_authentication('prod')}"
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    None
                ],
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/messages/0"),
        correlation_id
    )
