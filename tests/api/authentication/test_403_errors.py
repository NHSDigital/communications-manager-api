import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import VALID_ENDPOINTS

METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
CORRELATION_IDS = [None, "76491414-d0cf-4655-ae20-a4d1368472f3"]


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization(
    access="healthcare_worker",
    level="aal3",
    login_form={"username": "656005750104"},
    authentication="separate",
)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_user_token_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers, method, endpoints):
    """
    .. include:: ../partials/authentication/test_user_token_get.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        **nhsd_apim_auth_headers,
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        403,
        Generators.generate_forbidden_error() if method not in ["options", "head"] else None,
        None
    )
