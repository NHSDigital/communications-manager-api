import requests
import pytest
from lib import Assertions, Generators
from lib.constants import METHODS, CORRELATION_IDS

FORBIDDEN_TOKEN = {
    "Authorization": "Bearer ClientNotRecognised"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_403_forbidden(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        forbidden authorization token receives a 403 'Forbidden' response

        | **Given** the API consumer provides an forbidden authorization token
        | **When** the request is submitted
        | **Then** the response is a 403 forbidden error

    **Asserts**
    - Response returns a 403 'Forbidden' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
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
def test_403_forbidden_prefer(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. py:function:: Scenario: An API comsumer submitting a request with a \
        403 prefer header receives a 403 'Forbidden' response

        | **Given** the API consumer provides a 403 prefer header
        | **When** the request is submitted
        | **Then** the response is a 403 forbidden error

    **Asserts**
    - Response returns a 403 'Forbidden' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        "Prefer": "code=403",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_forbidden_error() if method not in ["options", "head"] else None,
        correlation_id
    )
