import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators, Authentication
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, DUPLICATE_PROPERTIES_PATHS, TOO_FEW_PROPERTIES_PATHS, MESSAGE_BATCHES_ENDPOINT

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
INVALID_MESSAGE_VALUES = [""]
INVALID_NHS_NUMBER = ["012345678"]
INVALID_DOB = ["1990-10-1"]


@pytest.mark.prodtest
def test_invalid_body():
    """
    .. include:: ../../partials/validation/test_invalid_body.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
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
@pytest.mark.parametrize("property, pointer", MISSING_PROPERTIES_PATHS)
def test_property_missing(property, pointer):
    """
    .. include:: ../../partials/validation/test_message_batch_property_missing.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", NULL_PROPERTIES_PATHS)
def test_data_null(property, pointer):
    """
    .. include:: ../../partials/validation/test_message_batch_null.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", INVALID_PROPERTIES_PATHS)
def test_data_invalid(property, pointer):
    """
    .. include:: ../../partials/validation/test_message_batch_invalid.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", DUPLICATE_PROPERTIES_PATHS)
def test_data_duplicate(property, pointer):
    """
    .. include:: ../../partials/validation/test_data_duplicate.rst
    """
    # Add a duplicate message to the payload to trigger the duplicate error
    data = Generators.generate_valid_create_message_batch_body()
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_duplicate_value_error(pointer),
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", TOO_FEW_PROPERTIES_PATHS)
def test_data_too_few_items(property, pointer):
    """
    .. include:: ../../partials/validation/test_data_too_few_items.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}",
        headers={
            **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("nhs_number", INVALID_NHS_NUMBER)
def test_invalid_nhs_number(nhs_number):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("dob", INVALID_DOB)
def test_invalid_dob(dob):
    """
    .. include:: ../../partials/validation/test_invalid_dob.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
def test_invalid_routing_plan():
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
def test_invalid_message_batch_reference():
    """
    .. include:: ../../partials/validation/test_invalid_message_batch_reference.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
def test_invalid_message_reference():
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("invalid_value", INVALID_MESSAGE_VALUES)
def test_blank_value_under_messages(invalid_value):
    """
    .. include:: ../../partials/validation/test_blank_value_under_messages.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
def test_null_value_under_messages():
    """
    .. include:: ../../partials/validation/test_null_value_under_messages.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", constants.INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", constants.NULL_VALUES)
def test_null_personalisation(personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(f"{constants.PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **headers,
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
        None
    )
