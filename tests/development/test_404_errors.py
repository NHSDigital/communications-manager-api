import requests
import pytest
from lib import Assertions, Generators

POST_PATHS = ["/v1/ignore/i-dont-exist", "/api/fake-endpoint", "/im-a-teapot"]
CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.devtest
@pytest.mark.parametrize("request_path", POST_PATHS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_404_not_found(nhsd_apim_proxy_url, request_path, correlation_id, method, nhsd_apim_auth_headers):
    """
    .. include:: ../../partials/not_found/test_404_not_found.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
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
