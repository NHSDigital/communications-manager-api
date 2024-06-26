import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    SINGLE_PAGE_ODS_CODES, CORRELATION_IDS

REPORT_NOT_FOUND_PAGE_NUMBERS = [2, 3, 4, 5, 6]
NOT_FOUND_ODS_CODE = 'T00404'


@pytest.mark.sandboxtest
@pytest.mark.parametrize("ods_code", SINGLE_PAGE_ODS_CODES)
@pytest.mark.parametrize("page", REPORT_NOT_FOUND_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_404_page_not_found(nhsd_apim_proxy_url, ods_code, page, correlation_id):

    """
    .. include:: ../../partials/not_found/test_404_nhsapp_accounts_page_not_found.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_404_report_not_found(nhsd_apim_proxy_url, correlation_id):

    """
    .. include:: ../../partials/not_found/test_404_nhsapp_accounts_report_not_found.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: NOT_FOUND_ODS_CODE,
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_REPORT_NOT_FOUND),
        correlation_id
    )
