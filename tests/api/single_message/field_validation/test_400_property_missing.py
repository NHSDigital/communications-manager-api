import requests
import pytest
from lib import Assertions, Permutations, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT, MISSING_PROPERTIES_PATHS


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", MISSING_PROPERTIES_PATHS)
def test_property_missing(url, bearer_token, property, pointer):
    """
    .. include:: ../partials/validation/test_messages_property_missing.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_missing_value_error(pointer),
        None
    )
