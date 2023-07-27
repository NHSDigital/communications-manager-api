import pytest
import requests
from lib import Assertions, Generators


CORRELATION_IDS = [None, "b1ad9302-5df9-4066-bcd2-b274cfab1e72"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_503_service_unavailable(nhsd_apim_proxy_url, correlation_id):
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
