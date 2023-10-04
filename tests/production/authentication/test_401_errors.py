import requests
import pytest
from lib import Assertions, Generators
from lib.constants import *


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', TOKENS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid(invalid_token, correlation_id, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an \
        invalid authentication token receives a 401 'Access Denied' response

        | **Given** the API consumer provides an invalid authentication token
        | **When** the request is submitted
        | **Then** the response is a 401 access denied error

    **Asserts**
    - Response returns a 401 'Access Denied' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(PROD_URL, headers={
        "Authorization": invalid_token,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )
