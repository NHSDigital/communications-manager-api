import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_message_id_that_does_not_exist(url, bearer_token):
    """
    .. include:: ../partials/not_found/test_message_id_that_does_not_exist.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(f"{url}{MESSAGES_ENDPOINT}/does-not-exist", headers=headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )
