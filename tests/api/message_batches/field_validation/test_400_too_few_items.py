import requests
import pytest
from lib import Assertions, Permutations, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.message_batches_paths import TOO_FEW_PROPERTIES_PATHS,  MESSAGE_BATCHES_ENDPOINT


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("property, pointer", TOO_FEW_PROPERTIES_PATHS)
def test_data_too_few_items(url, bearer_token, property, pointer):
    """
    .. include:: ../partials/validation/test_data_too_few_items.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("dev"),
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
