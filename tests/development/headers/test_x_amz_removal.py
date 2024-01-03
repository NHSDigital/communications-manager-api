import requests
import pytest

from lib import Assertions
from lib.constants.constants import VALID_ENDPOINTS, ORIGIN, TEST_METHODS


@pytest.mark.devtest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_with_x_amz_is_removed(nhsd_apim_proxy_url, endpoints, method, nhsd_apim_auth_headers,):

    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{endpoints}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })

    Assertions.assert_no_aws_headers(resp)
