import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants.constants import *

POST_PATHS = ["/v1/ignore/i-dont-exist"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


@pytest.mark.prodtest
@pytest.mark.parametrize("request_path", POST_PATHS)
@pytest.mark.parametrize("method", METHODS)
def test_404_not_found(request_path, method):
    """
    .. include:: ../../partials/not_found/test_404_not_found.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}{request_path}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "Accept": "*/*",
        "Content-Type": "application/json"
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error() if method not in ["options", "head"] else None,
        None
    )
