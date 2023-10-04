import requests
import pytest
from lib import Assertions, Generators
from lib.constants import CORRELATION_IDS, METHODS, TOKENS


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid_level(nhsd_apim_proxy_url, nhsd_apim_auth_headers, correlation_id, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an insufficient \
        level of authentication receives a 401 'Access Denied' response

        | **Given** the API consumer provides an insufficient level of authentication
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
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize('invalid_token', TOKENS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid(nhsd_apim_proxy_url, invalid_token, correlation_id, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an invalid \
        authentication token receives a 401 'Access Denied' response

        | **Given** the API consumer provides an invalid authentication
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
        "Authorization": invalid_token,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )
