import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import *
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', TOKENS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid(invalid_token, correlation_id, method):
    """
    .. include:: ../../partials/authentication/test_401_invalid.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": invalid_token,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )
