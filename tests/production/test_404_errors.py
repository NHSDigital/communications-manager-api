import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants import *

POST_PATHS = ["/v1/ignore/i-dont-exist", "/api/fake-endpoint", "/im-a-teapot"]
CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.prodtest
@pytest.mark.parametrize("request_path", POST_PATHS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_404_not_found(request_path, correlation_id, method):
    """
    .. py:function:: Scenario: An API consumer submitting a request to an unknown endpoint \
        receives a 404 'Not Found' response

        | **Given** the API consumer does not know how to identify the resource they want to fetch
        | **When** the request is submitted to an unknown resource
        | **Then** the service responds with a 404 not found response, telling the user the resource does not exist

    **Asserts**
    - Response returns a 404 'Not Found' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/methods.rst
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{request_path}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
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
