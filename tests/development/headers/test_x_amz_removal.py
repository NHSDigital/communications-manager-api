import requests
import pytest

from lib import Assertions
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import VALID_ENDPOINTS, ORIGIN, METHODS


@pytest.mark.devtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_amz_is_removed(nhsd_apim_proxy_url, bearer_token_internal_dev, endpoints, method,):

    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}/{endpoints}", headers={
        "Authorization": bearer_token_internal_dev.value,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })

    Assertions.assert_no_aws_headers(resp)
