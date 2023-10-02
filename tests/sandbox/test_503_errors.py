import pytest
import requests
from lib import Assertions, Generators


CORRELATION_IDS = [None, "b1ad9302-5df9-4066-bcd2-b274cfab1e72"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_503_service_unavailable(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        503 prefer header receives a 503 'Service Unavailable' response

        | **Given** the API consumer provides a 503 prefer header
        | **When** the request is submitted
        | **Then** the response is a 503 service unavailable error

    **Asserts**
    - Response returns a 503 'Service Unavailable' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        "Prefer": "code=503",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        503,
        Generators.generate_service_unavailable_error(),
        correlation_id
    )
