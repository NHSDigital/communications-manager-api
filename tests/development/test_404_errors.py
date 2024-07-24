import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR

ENDPOINT = "/v1/ignore/i-dont-exist"
CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_404_not_found(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id, method):
    """
    .. include:: ../../partials/not_found/test_404_not_found.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{ENDPOINT}", headers={
        "Authorization": bearer_token_internal_dev.value,
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
