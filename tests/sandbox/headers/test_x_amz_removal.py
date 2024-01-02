import requests
import pytest

from lib import Assertions
from lib.constants.constants import VALID_ENDPOINTS

TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_amz_is_removed( nhsd_apim_proxy_url, endpoints, method):

    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{endpoints}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_no_aws_headers(resp)
