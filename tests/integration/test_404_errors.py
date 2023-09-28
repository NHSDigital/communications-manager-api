import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants import INT_URL, METHODS, CORRELATION_IDS

POST_PATHS = ["/v1/ignore/i-dont-exist", "/api/fake-endpoint", "/im-a-teapot"]


@pytest.mark.devtest
@pytest.mark.parametrize("request_path", POST_PATHS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_404_not_found(request_path, correlation_id, method):
    """
    .. py:function:: Test 404 response
    """
    resp = getattr(requests, method)(f"{INT_URL}{request_path}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
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
