import requests
import pytest
from lib import Assertions, Generators, Authentication
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, CORRELATION_IDS

REPORT_NOT_FOUND_PAGE_NUMBERS = [1000, 2000, 3000]


@pytest.mark.prodtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", REPORT_NOT_FOUND_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_404_page_not_found(ods_code, page, correlation_id):

    """
    .. include:: ../../partials/not_found/test_404_nhsapp_accounts_page_not_found.rst
    """
    resp = requests.get(f"{constants.PROD_URL}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("prod"),
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
