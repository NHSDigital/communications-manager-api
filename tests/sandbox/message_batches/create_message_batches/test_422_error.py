import requests
import pytest
from lib import Assertions, Generators, error_handler

CORRELATION_IDS = [None, "0f160ae2-9b62-47bf-bdf0-c6a844d59488"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_duplicate_batch_request(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/duplicate_request/test_422_duplicate_request.rst
    """
    resp = requests.post(nhsd_apim_proxy_url, headers={
        "Prefer": "code=422_batch",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        422,
        Generators.generate_duplicate_batch_request_error(),
        correlation_id
    )
