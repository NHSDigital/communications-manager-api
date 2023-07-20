import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
CORRELATION_IDS = [None, "e8bb49c6-06bc-44f7-8443-9244284640f8"]
INVALID_MESSAGE_VALUES = ["", [], 5, 0.1]
NHS_NUMBER = ["012345678", "01234567890", "abcdefghij", "", [], {}, 5, 0.1]
DOB = ["1990-10-1", "1990-1-10", "90-10-10", "10-12-1990", "1-MAY-2000", "1990/01/01", "", [], {}, 5, 0.1]


"""
Invalid body 400 tests
"""


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_body(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
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


"""
Missing property 400 test
"""

_missing_properties = [
    ("data", "/data"),
    ("type", "/data/type"),
    ("attributes", "/data/attributes"),
    ("routingPlanId", "/data/attributes/routingPlanId"),
    ("messageBatchReference", "/data/attributes/messageBatchReference"),
    ("messages", "/data/attributes/messages"),
    ("messageReference", "/data/attributes/messages/0/messageReference"),
    ("recipient", "/data/attributes/messages/0/recipient"),
    ("nhsNumber", "/data/attributes/messages/0/recipient/nhsNumber"),
]


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    _missing_properties
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_property_missing(nhsd_apim_proxy_url, property, pointer, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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


"""
Null data 400 test
"""

_null_properties = [
    ("data", "/data"),
    ("attributes", "/data/attributes"),
    ("recipient", "/data/attributes/messages/0/recipient"),
]


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    _null_properties
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_null(nhsd_apim_proxy_url, property, pointer, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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


"""
Invalid data 400 test
"""

_invalid_properties = [
    ("type", "/data/type"),
    ("routingPlanId", "/data/attributes/routingPlanId"),
    ("messageBatchReference", "/data/attributes/messageBatchReference"),
    ("messages", "/data/attributes/messages"),
    ("messageReference", "/data/attributes/messages/0/messageReference"),
    ("recipient", "/data/attributes/messages/0/recipient"),
    ("nhsNumber", "/data/attributes/messages/0/recipient/nhsNumber"),
    ("dateOfBirth", "/data/attributes/messages/0/recipient/dateOfBirth"),
    ("personalisation", "/data/attributes/messages/0/personalisation"),
]


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    _invalid_properties
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_invalid(nhsd_apim_proxy_url, property, pointer, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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


"""
Duplicate data 400 test
"""

_duplicate_properties = [
    ("messageReference", "/data/attributes/messages/1/messageReference"),
]


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    _duplicate_properties
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_duplicate(nhsd_apim_proxy_url, property, pointer, correlation_id, nhsd_apim_auth_headers):
    # Add a duplicate message to the payload to trigger the duplicate error
    data = Generators.generate_valid_create_message_batch_body()
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
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


"""
Too few items 400 test
"""

_too_few_properties = [
    ("messages", "/data/attributes/messages"),
]


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    _too_few_properties
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_too_few_items(nhsd_apim_proxy_url, property, pointer, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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


@pytest.mark.inttest
@pytest.mark.parametrize("nhs_number", NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_nhs_number(nhsd_apim_proxy_url, nhs_number, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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
        Generators.generate_invalid_value_error("/data/attributes/messages/0/recipient/nhsNumber"),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("dob", DOB)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_dob(nhsd_apim_proxy_url, dob, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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
                            "nhsNumber": "0123456789",
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
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_routing_plan(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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
                            "nhsNumber": "0123456789",
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


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_message_batch_reference(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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
                            "nhsNumber": "0123456789",
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


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_message_reference(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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
                            "nhsNumber": "0123456789",
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


@pytest.mark.inttest
@pytest.mark.parametrize("invalid_value", INVALID_MESSAGE_VALUES)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_blank_value_under_messages(nhsd_apim_proxy_url, invalid_value, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_null_value_under_messages(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": correlation_id
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
