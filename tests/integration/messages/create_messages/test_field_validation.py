import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators
from lib.constants.constants import Error, INT_URL, INVALID_NHS_NUMBER, INVALID_DOB, \
    INVALID_PERSONALISATION_VALUES, NULL_VALUES, CORRELATION_IDS
from lib.constants.messages_paths import MISSING_PROPERTIES_PATHS, NULL_PROPERTIES_PATHS, \
    INVALID_PROPERTIES_PATHS, MESSAGES_ENDPOINT
from lib.fixtures import *  # NOSONAR


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_body(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_body.rst
    """
    resp = requests.post(
        f"{INT_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
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


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    MISSING_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_property_missing(bearer_token_int, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_property_missing.rst
    """
    resp = requests.post(
        f"{INT_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
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


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    NULL_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_data_null(bearer_token_int, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_null.rst
    """
    resp = requests.post(
        f"{INT_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
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


@pytest.mark.inttest
@pytest.mark.parametrize(
    "property, pointer",
    INVALID_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_data_invalid(bearer_token_int, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_messages_invalid.rst
    """
    resp = requests.post(
        f"{INT_URL}{MESSAGES_ENDPOINT}",
        headers={
            "Authorization": bearer_token_int.value,
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


@pytest.mark.inttest
@pytest.mark.parametrize("nhs_number", INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_nhs_number(bearer_token_int, nhs_number, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": nhs_number,
                    "dateOfBirth": "2023-01-01"
                },
                "personalisation": {}

            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_nhs_number_error("/data/attributes/recipient/nhsNumber"),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("dob", INVALID_DOB)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_dob(bearer_token_int, dob, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_dob.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "2023-01-01"
                },
                "personalisation": {}

            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/recipient/dateOfBirth"),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_routing_plan(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "invalid",
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "2023-01-01"
                },
                "personalisation": {}

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
def test_invalid_message_reference(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": "invalid",
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "2023-01-01"
                },
                "personalisation": {}
            }

        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messageReference"),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", INVALID_PERSONALISATION_VALUES)
def test_invalid_personalisation(bearer_token_int, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": "invalid",
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "2023-01-01"
                },
                "personalisation": personalisation
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/personalisation"),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("personalisation", NULL_VALUES)
def test_null_personalisation(bearer_token_int, correlation_id, personalisation):
    """
    .. include:: ../../partials/validation/test_invalid_personalisation.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": "invalid",
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "2023-01-01"
                },
                "personalisation": personalisation
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/personalisation"),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_sms_contact_details(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_sms.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "2023-01-01",
                    "contactDetails": {
                        "sms": "07700900002"
                    }
                },
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/sms",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_email_contact_details(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_email.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "2023-01-01",
                    "contactDetails": {
                        "email": "invalidEmailAddress"
                    }
                },
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/email",
            "Input failed format check"
        ),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_address_contact_details_too_few_lines(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_few.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": str(uuid.uuid1()),
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
        }
    })

    error = Error(
        "CM_MISSING_VALUE",
        "400",
        "Missing value",
        "Too few address lines were provided"
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(error, source={
            "pointer": "/data/attributes/recipient/contactDetails/address"
        }),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_address_contact_details_too_many_lines(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_lines_too_many.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageReference": str(uuid.uuid1()),
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
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/address",
            "Invalid"
        ),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_address_contact_details_postcode(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_contact_details_address_postcode.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        **headers,
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
                "messageReference": str(uuid.uuid1()),
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
                                "5"
                            ],
                            "postcode": "LS1 6AECD"
                        }
                    }
                },
                "personalisation": {}
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/recipient/contactDetails/address",
            "Postcode input failed format check"
        ),
        correlation_id
    )
