import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import ERROR_CANNOT_SET_CONTACT_DETAILS
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_sms_contact_details(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_contact_details_sms.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"] = {
        "contactDetails": {
            "sms": 1234
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/sms",
            "'sms' is not a string"
        ),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_sms_contact_details_second_message(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_contact_details_sms.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][1]["recipient"] = {
        "contactDetails": {
            "sms": 1234
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/1/recipient/contactDetails/sms",
            "'sms' is not a string"
        ),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_email_contact_details(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_contact_details_email.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"] = {
        "contactDetails": {
            "email": 1234
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/email",
            "'email' is not a string"
        ),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_email_contact_details_third_message(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_contact_details_email.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][2]["recipient"] = {
        "contactDetails": {
            "email": 1234
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/2/recipient/contactDetails/email",
            "'email' is not a string"
        ),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_address_contact_details_too_many_lines(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_contact_details_address_lines_too_many.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2", "3", "4", "5", "6"],
            "postcode": "LS1 6AE"
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/address",
            "Too many address lines were provided"
        ),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_address_contact_details_lines_not_string_array(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_contact_details_address_lines.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "address": {
            "lines": [1, 2, 3],
            "postcode": "LS1 6AE"
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/address",
            "Field 'address': 'lines' is not a string array"
        ),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_invalid_address_contact_details_postcode_not_string(url, bearer_token):
    """
    .. include:: ../partials/validation/test_invalid_contact_details_address_lines.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "address": {
            "lines": ["1", "2"],
            "postcode": []
        }
    }

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error_custom_detail(
            "/data/attributes/messages/0/recipient/contactDetails/address",
            "Field 'address': 'postcode' is not a string"
        ),
        None
    )


@pytest.mark.devtest
def test_not_permitted_to_use_contact_details(url, bearer_token_internal_dev_test_1):
    """
    .. include:: ../partials/validation/test_not_permitted_to_use_contact_details.rst
    """
    headers = Generators.generate_valid_headers(bearer_token_internal_dev_test_1.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["routingPlanId"] = "558a52ab-9d48-406e-9815-7fd517df5b9e"
    data["data"]["attributes"]["messages"][0]["recipient"]["contactDetails"] = {
        "sms": "07777777777",
        "email": "ab@cd.co.uk",
        "address": {
            "lines": ["Line 1", "Line 2"],
            "postcode": "LS7 1BN"
        }
    }
    del data["data"]["attributes"]["messages"][0]["originator"]

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(
            ERROR_CANNOT_SET_CONTACT_DETAILS,
            source={
                "pointer": "/data/attributes/messages/0/recipient/contactDetails"
                }
                ),
        None
    )
