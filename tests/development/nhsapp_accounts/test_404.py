import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, CORRELATION_IDS

INVALID_PAGE_NUMBERS = [1000, 2000, 3000]


@pytest.mark.devtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", INVALID_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_404_page_not_found(nhsd_apim_proxy_url, nhsd_apim_auth_headers, ods_code, page, correlation_id):

    """
    .. include:: ../../partials/not_found/test_404_nhsapp_accounts_page_not_found.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_REPORT_NOT_FOUND),
        correlation_id
    )
