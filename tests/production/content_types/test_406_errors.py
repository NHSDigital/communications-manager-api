import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import METHODS, PROD_URL, VALID_ENDPOINTS
from lib.fixtures import *  # NOSONAR


@pytest.mark.prodtest
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
@pytest.mark.parametrize("method", METHODS)
def test_406(bearer_token_prod, method, endpoints):
    """
    .. include:: ../../partials/content_types/test_406.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}/{endpoints}", headers={
        "Accept": "invalid",
        "Authorization": bearer_token_prod.value,
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        406,
        Generators.generate_not_acceptable_error() if method not in ["options", "head"] else None,
        None
    )
