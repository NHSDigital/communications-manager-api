import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, CORRELATION_IDS
from lib.fixtures import *  # NOSONAR

REPORT_NOT_FOUND_PAGE_NUMBERS = [1000, 2000, 3000]
NOT_FOUND_ODS_CODE = 'T00404'


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", REPORT_NOT_FOUND_PAGE_NUMBERS)
def test_404_page_not_found(url, bearer_token, ods_code, page):

    """
    .. include:: ../partials/not_found/test_404_nhsapp_accounts_page_not_found.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{NHSAPP_ACCOUNTS_ENDPOINT}",
        headers=headers,
        params={
            ODS_CODE_PARAM_NAME: ods_code,
            PAGE_PARAM_NAME: page
        })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_REPORT_NOT_FOUND),
        None
    )
