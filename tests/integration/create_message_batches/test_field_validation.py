import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators, Authentication
import lib.constants as constants

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
INVALID_MESSAGE_VALUES = ["", [], 5, 0.1]
INVALID_NHS_NUMBER = ["999054860", "99905486090", "abcdefghij", "", [], {}, 5, 0.1]
INVALID_DOB = ["1990-10-1", "1990-1-10", "90-10-10", "10-12-1990", "1-MAY-2000", "1990/01/01", "", [], {}, 5, 0.1]


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_body(correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request without a request body \
        receives a 400 'Invalid Value' response

        | **Given** the API consumer provides an empty message body
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(
        f"{constants.INT_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
        },
        data="{}SF{}NOTVALID",
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/"),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    constants.MISSING_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_property_missing(property, pointer, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request without a required attribute \
        in the request body receives a 400 'Missing Value' response

        | **Given** the API consumer provides an message body with a missing required attribute
        | **When** the request is submitted
        | **Then** the response returns a 400 missing value error

    **Asserts**
    - Response returns a 400 'Missing Value' error
    - Response returns the expected error message body with references to the missing attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/request_properties.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(
        f"{constants.INT_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_batch_body("int"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_missing_value_error(pointer),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    constants.NULL_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_null(property, pointer, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an empty required attribute \
        in the request body receives a 400 'Null Value' response

        | **Given** the API consumer provides an message body with a null attribute
        | **When** the request is submitted
        | **Then** the response returns a 400 null value error

    **Asserts**
    - Response returns a 400 'Null Value' error
    - Response returns the expected error message body with references to the null attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/request_properties.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(
        f"{constants.INT_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_batch_body("int"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error(pointer),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    constants.INVALID_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_invalid(property, pointer, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid required attribute \
        in the request body receives a 400 'Invalid Value' response

        | **Given** the API consumer provides an message body with an invalid attribute
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body with references to the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/request_properties.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(
        f"{constants.INT_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("int"),
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


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    constants.DUPLICATE_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_duplicate(property, pointer, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a duplicate attribute \
        in the request body receives a 400 'Duplicate Value' response

        | **Given** the API consumer provides an message body with duplicate attributes
        | **When** the request is submitted
        | **Then** the response returns a 400 duplicate value error

    **Asserts**
    - Response returns a 400 'Duplicate Value' error
    - Response returns the expected error message body with references to the duplicate attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/request_properties.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    # Add a duplicate message to the payload to trigger the duplicate error
    data = Generators.generate_valid_create_message_batch_body("int")
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{constants.INT_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
        },
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_duplicate_value_error(pointer),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    constants.TOO_FEW_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_too_few_items(property, pointer, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with too few attributes \
        in the request body receives a 400 'Invalid Value' response

        | **Given** the API consumer provides an message body with too few attributes
        | **When** the request is submitted
        | **Then** the response returns a 400 too few items error

    **Asserts**
    - Response returns a 400 'Too Few Items' error
    - Response returns the expected error message body with references to the removed attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/request_properties.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(
        f"{constants.INT_URL}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("int"),
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


@pytest.mark.inttest
@pytest.mark.parametrize("nhs_number", INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_nhs_number(nhs_number, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
        NHS number receives a 400 'Invalid NHS Number' response

        An NHS Number is a 10 digit number used to identify patients, for more \
            information on the structure of NHS numbers look \
                `here <https://www.datadictionary.nhs.uk/attributes/nhs_number.html>`__

        | **Given** the API consumer provides an message body with an invalid NHS number
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid nhs number error

    **Asserts**
    - Response returns a 400 'Invalid NHS Number' error
    - Response returns the expected error message body with references to the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{constants.INT_URL}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
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
                            "dateOfBirth": "2023-01-01"
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
        Generators.generate_invalid_nhs_number_error(constants.FIRST_MESSAGE_RECIPIENT_NHSNUMBER_PATH),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("dob", INVALID_DOB)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_dob(dob, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
        date of birth receives a 400 'Invalid Value' response

        A valid date of birth must be structured in this format: YYYY-MM-dd

        | **Given** the API consumer provides an message body with an invalid date of birth
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body with references to the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{constants.INT_URL}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
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


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_routing_plan(correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
       routing plan receives a 400 'Invalid Value' response

        The routing plan must be in a UUID format, for more information on UUID, \
            look `here <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__

        | **Given** the API consumer provides an message body with an invalid routing plan
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body with references to the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{constants.INT_URL}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
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
                            "dateOfBirth": "2023-01-01"
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
        Generators.generate_invalid_value_error(constants.ROUTING_PLAN_ID_PATH),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_batch_reference(correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
        message batch reference receives a 400 'Invalid Value' response

        The message batch reference must be in a UUID format, for more information on UUID, \
            look `here <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__

        | **Given** the API consumer provides an message body with an invalid message batch reference
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body with references to the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{constants.INT_URL}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
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
                            "dateOfBirth": "2023-01-01"
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
        Generators.generate_invalid_value_error(constants.MESSAGE_BATCH_REFERENCE_PATH),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_reference(correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
        message reference receives a 400 'Invalid Value' response

        The message reference must be in a UUID format, for more information on UUID, \
            look `here <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__

        | **Given** the API consumer provides an message body with an invalid message reference
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body with references to the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{constants.INT_URL}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
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
                            "dateOfBirth": "2023-01-01"
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
        Generators.generate_invalid_value_error(constants.FIRST_MESSAGE_REFERENCE_PATH),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("invalid_value", INVALID_MESSAGE_VALUES)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_blank_value_under_messages(invalid_value, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
        message value receives a 400 'Invalid Value' response

        | **Given** the API consumer provides an message body with an invalid message value
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body with references to the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{constants.INT_URL}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
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


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_null_value_under_messages(correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a null \
        message value receives a 400 'Null Value' response

        | **Given** the API consumer provides an message body with a null message value
        | **When** the request is submitted
        | **Then** the response returns a 400 null value error

    **Asserts**
    - Response returns a 400 'Null Value' error
    - Response returns the expected error message body with references to the null attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{constants.INT_URL}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('int')}"
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
