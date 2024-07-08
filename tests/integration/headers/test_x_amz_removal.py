import requests
import pytest

from lib import Assertions
from lib.constants.constants import VALID_ENDPOINTS, ORIGIN, METHODS, INT_URL
from lib.fixtures import *


@pytest.mark.inttest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_amz_is_removed(bearer_token_int, endpoints, method):

    resp = getattr(requests, method)(f"{INT_URL}/{endpoints}", headers={
        "Authorization": bearer_token_int.value,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })

    Assertions.assert_no_aws_headers(resp)
