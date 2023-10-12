import requests
import pytest
from lib import Assertions, Generators
from lib.constants import MESSAGES_ENDPOINT

CORRELATION_IDS = [None, "b1ad9302-5df9-4066-bcd2-b274cfab1e72"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_408_timeout_prefer(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/timeouts/test_408_timeout_prefer.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
        "Prefer": "code=408",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        408,
        Generators.generate_request_timeout_error(),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_504_timeout_prefer(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/timeouts/test_504_timeout_prefer.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
        "Prefer": "code=504",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        504,
        Generators.generate_service_timeout_error(),
        correlation_id
    )
