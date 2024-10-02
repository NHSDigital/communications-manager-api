import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, DUPLICATE_PROPERTIES_PATHS, TOO_FEW_PROPERTIES_PATHS, MESSAGE_BATCHES_ENDPOINT
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_body(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_body.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    MISSING_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_property_missing(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_message_batch_property_missing.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_batch_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_missing_value_error(pointer),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    NULL_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_null(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_message_batch_null.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_batch_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error(pointer),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    INVALID_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_invalid(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_message_batch_invalid.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("sandbox"),
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    DUPLICATE_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_duplicate(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_duplicate.rst
    """
    # Add a duplicate message to the payload to trigger the duplicate error
    data = Generators.generate_valid_create_message_batch_body("sandbox")
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    TOO_FEW_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_data_too_few_items(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_too_few_items.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("sandbox"),
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize("nhs_number", constants.INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_nhs_number(nhsd_apim_proxy_url, nhs_number, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
        Generators.generate_invalid_nhs_number_error("/data/attributes/messages/0/recipient/nhsNumber"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("dob", constants.INVALID_DOB)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_dob(nhsd_apim_proxy_url, dob, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_dob.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_routing_plan(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_batch_reference(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_batch_reference.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
        Generators.generate_invalid_value_error("/data/attributes/messageBatchReference"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_invalid_message_reference(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
        Generators.generate_invalid_value_error("/data/attributes/messages/0/messageReference"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("invalid_value", constants.INVALID_MESSAGE_VALUES)
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_blank_value_under_messages(nhsd_apim_proxy_url, invalid_value, correlation_id):
    """
    .. include:: ../../partials/validation/test_blank_value_under_messages.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
def test_null_value_under_messages(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_null_value_under_messages.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("number_of_errors", [99, 100, 101, 150, 200])
def test_validation_returns_at_max_errors(nhsd_apim_proxy_url, correlation_id, number_of_errors):
    """
    .. include:: ../../partials/validation/test_validation_returns_at_max_errors.rst
    """
    duplicate_message_reference = str(uuid.uuid4())
    data = {
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": duplicate_message_reference,
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": {}
                    } for _ in range(number_of_errors)
                ],
            }
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data,
    )
    assert len(resp.json().get("errors")) <= constants.NUM_MAX_ERRORS


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(nhsd_apim_proxy_url, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": personalisation
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messages/0/personalisation"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", constants.NULL_VALUES)
def test_null_personalisation(nhsd_apim_proxy_url, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": personalisation
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/messages/0/personalisation"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_not_permitted_to_use_contact_details(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_not_permitted_to_use_contact_details.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
        "X-Correlation-Id": correlation_id,
        "Authorization": "notAllowedContactDetailOverride"
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
                            "dateOfBirth": "2023-01-01",
                            "contactDetails": {
                                "sms": "07700900002"
                            }
                        },
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(
            constants.ERROR_CANNOT_SET_CONTACT_DETAILS,
            source={
                "pointer": "/data/attributes/messages/0/recipient/contactDetails"
                }
                ),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_sms_contact_details(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_sms.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01",
                            "contactDetails": {
                                "sms": "07700900002"
                            }
                        },
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/sms",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_email_contact_details(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_email.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01",
                            "contactDetails": {
                                "email": "invalidEmailAddress"
                            }
                        },
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/email",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_address_contact_details_too_few_lines(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_few.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01",
                            "contactDetails": {
                                "address": {
                                    "lines": [
                                        "1"
                                    ],
                                    "postcode": "test"
                                }
                            }
                        },
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_too_few_items_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/address",
            "Too few address lines were provided"
        ),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", constants.CORRELATION_ID)
def test_invalid_address_contact_details_too_many_lines(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_many.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
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
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01",
                            "contactDetails": {
                                "address": {
                                    "lines": [
                                        "1",
                                        "2",
                                        "3",
                                        "4",
                                        "5",
                                        "6"
                                    ],
                                    "postcode": "test"
                                }
                            }
                        },
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/address",
            "Invalid"
        ),
        correlation_id
    )
