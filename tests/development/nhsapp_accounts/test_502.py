import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    SINGLE_PAGE_ODS_CODES, CORRELATION_IDS

BAD_GATEWAY_ODS_CODE = 'T00401'  # The mock for the NHS App API will return a 401 should cause the BE to return a 502


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_502_bad_gateway(nhsd_apim_proxy_url, correlation_id):

    """
    .. include:: ../../partials/bad_gatway/test_502_bad_gateway.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: BAD_GATEWAY_ODS_CODE,
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        502,
        Generators.generate_bad_gateway_error,
        correlation_id
    )
