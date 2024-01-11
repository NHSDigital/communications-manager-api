import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import METHODS, VALID_ENDPOINTS, PROD_URL


@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_401_invalid(method, endpoints):
    """
    .. include:: ../../partials/authentication/test_401_invalid.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{endpoints}", headers={
        "Authorization": "invalid"
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        None
    )
