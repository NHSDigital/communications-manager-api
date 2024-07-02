import requests
import pytest

from lib import Assertions, Authentication
from lib.constants.constants import VALID_ENDPOINTS, ORIGIN, METHODS, INT_URL


@pytest.mark.inttest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_amz_is_removed(endpoints, method):

    resp = getattr(requests, method)(f"{INT_URL}/{endpoints}", headers={
        "Authorization": f"{Authentication.generate_authentication('int')}",
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })

    Assertions.assert_no_aws_headers(resp)
