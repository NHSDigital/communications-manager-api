import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import INT_URL, METHODS, CORRELATION_IDS
from lib.fixtures import *  # NOSONAR

ENDPOINT = "/v1/ignore/i-dont-exist"


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_404_not_found(bearer_token_int, correlation_id, method):
    """
    .. include:: ../../partials/not_found/test_404_not_found.rst
    """
    resp = getattr(requests, method)(f"{INT_URL}{ENDPOINT}", headers={
        "Authorization": bearer_token_int.value,
        "X-Correlation-Id": correlation_id,
        "Accept": "*/*",
        "Content-Type": "application/json"
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error() if method not in ["options", "head"] else None,
        correlation_id
    )
