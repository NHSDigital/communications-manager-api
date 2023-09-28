import requests
import pytest
from lib import Assertions, Generators

REQUEST_PATH = "/v1/message-batches"
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
CORRELATION_IDS = [None, "76491414-d0cf-4655-ae20-a4d1368472f3"]


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_user_token_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers, correlation_id, method):
    """
    .. py:function:: Test 403 user token not acceptable
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_forbidden_error() if method not in ["options", "head"] else None,
        correlation_id
    )
