import requests
import pytest
from lib import Assertions, Generators
from tests.lib.constants import *


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid_level(nhsd_apim_proxy_url, nhsd_apim_auth_headers, correlation_id, method):
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize('invalid_token', TOKENS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid(nhsd_apim_proxy_url, invalid_token, correlation_id, method):
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        "Authorization": invalid_token,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )
