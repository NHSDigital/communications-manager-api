import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import METHODS, VALID_ENDPOINTS
from lib.fixtures import *  # NOSONAR


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_401_invalid(url, method, endpoints):
    """
    .. include:: ../partials/authentication/test_401_invalid.rst
    """
    resp = getattr(requests, method)(f"{url}{endpoints}", headers={
        "Authorization": "invalid",
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        None
    )


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("endpoints", VALID_ENDPOINTS)
def test_401_invalid_level(nhsd_apim_proxy_url, nhsd_apim_auth_headers, method, endpoints):
    """
    .. include:: ../partials/authentication/test_401_invalid_level.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}{endpoints}", headers={
        **nhsd_apim_auth_headers
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        None
    )
