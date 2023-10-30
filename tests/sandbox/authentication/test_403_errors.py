import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import METHODS, CORRELATION_IDS, VALID_ENDPOINTS

FORBIDDEN_TOKEN = {
    "Authorization": "Bearer ClientNotRecognised"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_403_forbidden(nhsd_apim_proxy_url, correlation_id, method, endpoints):
    """
    .. include:: ../../partials/authentication/test_403_forbidden.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_forbidden_error() if method not in ["options", "head"] else None,
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_403_forbidden_prefer(nhsd_apim_proxy_url, correlation_id, method, endpoints):
    """
    .. include:: ../../partials/authentication/test_403_forbidden_prefer.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        "Prefer": "code=403",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_forbidden_error() if method not in ["options", "head"] else None,
        correlation_id
    )
