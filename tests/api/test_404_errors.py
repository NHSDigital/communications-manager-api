import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR

ENDPOINT = "/v1/ignore/i-dont-exist"
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.devtest
@pytest.mark.parametrize("method", METHODS)
def test_404_not_found(url, bearer_token, method):
    """
    .. include:: ../partials/not_found/test_404_not_found.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = getattr(requests, method)(f"{url}{ENDPOINT}", headers=headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error() if method not in ["options", "head"] else None,
        None
    )
