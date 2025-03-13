import requests
import pytest
from lib import Assertions, Permutations, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import NULL_PROPERTIES_PATHS, MESSAGES_ENDPOINT
from lib.constants.constants import NULL_VALUES


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", NULL_PROPERTIES_PATHS)
def test_data_null(url, bearer_token, property, pointer):
    """
    .. include:: ../partials/validation/test_messages_null.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error(pointer),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("personalisation", NULL_VALUES)
def test_null_personalisation(url, bearer_token, personalisation):
    """
    .. include:: ../partials/validation/test_invalid_personalisation.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["personalisation"] = personalisation

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/personalisation"),
        None
    )
