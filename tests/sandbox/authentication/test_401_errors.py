import requests
import pytest
from lib import Assertions, Generators
from lib.constants import *


MOCK_TOKEN = {
    "Authorization": "Bearer InvalidMockToken"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an \
        invalid authorization token receives a 401 'Access Denied' response

        | **Given** the API consumer provides an invalid authorization token
        | **When** the request is submitted
        | **Then** the response is a 401 access denied error

    **Asserts**
    - Response returns a 401 'Access Denied' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
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
    .. py:function:: Scenario: An API consumer submitting a request with a 401 prefer header \
        receives a 401 'Access Denied' response

        | **Given** the API consumer provides a 401 prefer header
        | **When** the request is submitted
        | **Then** the response is a 401 access denied error

    **Asserts**
    - Response returns a 401 'Access Denied' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        "Prefer": "code=401",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )
