import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.message_batches_paths import DUPLICATE_PROPERTIES_PATHS, MESSAGE_BATCHES_ENDPOINT


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", DUPLICATE_PROPERTIES_PATHS)
def test_data_duplicate(url, bearer_token, property, pointer):
    """
    .. include:: ../partials/validation/test_data_duplicate.rst
    """
    # Add a duplicate message to the payload to trigger the duplicate error
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_duplicate_value_error(pointer),
        None
    )
