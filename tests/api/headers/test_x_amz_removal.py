import requests
import pytest

from lib import Assertions
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import VALID_ENDPOINTS, ORIGIN, METHODS


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_request_with_x_amz_is_removed(url, bearer_token, endpoints, method):
    """
    .. include:: ../partials/headers/test_request_with_x_amz_is_removed.rst
    """
    resp = getattr(requests, method)(f"{url}/{endpoints}", headers={
        "Authorization": bearer_token.value,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })

    Assertions.assert_no_aws_headers(resp)
