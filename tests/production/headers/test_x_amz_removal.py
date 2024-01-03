import requests
import pytest

from lib import Assertions, Authentication
from lib.constants.constants import VALID_ENDPOINTS, ORIGIN, TEST_METHODS


@pytest.mark.prodtest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_amz_is_removed(nhsd_apim_proxy_url, endpoints, method):

    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })

    Assertions.assert_no_aws_headers(resp)
