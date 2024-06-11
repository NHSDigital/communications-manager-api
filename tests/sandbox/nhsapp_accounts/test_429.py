import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    SINGLE_PAGE_ODS_CODES, CORRELATION_IDS

TOO_MANY_REQUESTS_ODS_CODE = 'T00429'


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_429_too_many_requests(nhsd_apim_proxy_url, correlation_id):

    """
    .. include:: ../../partials/too_many_requests/test_429_too_many_requests.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: TOO_MANY_REQUESTS_ODS_CODE,
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error(),
        correlation_id
    )
