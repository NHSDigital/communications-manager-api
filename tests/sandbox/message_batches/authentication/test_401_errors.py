import requests
import pytest
from lib import Assertions, Generators
from lib.constants import CORRELATION_IDS, METHODS, MESSAGE_BATCHES_ENDPOINT


MOCK_TOKEN = {
    "Authorization": "Bearer InvalidMockToken"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. include:: ../../partials/authentication/test_401_invalid.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid_prefer(nhsd_apim_proxy_url, correlation_id, method):
    """
    ..include:: ../../partials/authentication/test_401_invalid_prefer.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Prefer": "code=401",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )
