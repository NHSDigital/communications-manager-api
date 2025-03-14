import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.constants import VALID_ENDPOINTS

CONTENT_TYPE_NAME = ["content-type", "conTENT_tYpe"]
CONTENT_TYPE_VALUE = ["", "image/png", "application/json; charset=utf-9"]
METHODS = ["post", "put", "patch"]
CORRELATION_IDS = [None, "88b10816-5d45-4992-bed0-ea685aaa0e1f"]


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("content_type_name", CONTENT_TYPE_NAME)
@pytest.mark.parametrize("content_type_value", CONTENT_TYPE_VALUE)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_415_invalid(
    url,
    bearer_token,
    content_type_name,
    content_type_value,
    correlation_id,
    method,
    endpoints
):
    """
    .. include:: ../partials/content_types/test_415_invalid.rst
    """
    resp = getattr(requests, method)(f"{url}{endpoints}", headers={
        "Authorization": bearer_token.value,
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        415,
        Generators.generate_unsupported_media_error(),
        correlation_id
    )
