import requests
import pytest

from lib import Assertions
from lib.constants.constants import VALID_ENDPOINTS, ORIGIN, METHODS
from lib.fixtures import *


# Add prodtest once 4.9.0 is in prod
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_amz_is_removed(bearer_token_prod, nhsd_apim_proxy_url, endpoints, method):

    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{endpoints}", headers={
        "Authorization": bearer_token_prod.value,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })

    Assertions.assert_no_aws_headers(resp)
