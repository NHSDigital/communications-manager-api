import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import CORRELATION_IDS, PROD_URL, VALID_ENDPOINTS
from lib.fixtures import *

METHODS = ["post", "put", "patch"]


@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_415_invalid(bearer_token_prod, method, endpoints):
    """
    .. include:: ../../partials/content_types/test_415_invalid.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{endpoints}", headers={
        "Authorization": bearer_token_prod,
        "Accept": "application/json",
        "Content-Type": "invalid"
        })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        415,
        Generators.generate_unsupported_media_error(),
        None
    )
