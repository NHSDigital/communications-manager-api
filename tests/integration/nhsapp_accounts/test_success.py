import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants.constants import INT_URL
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, CORRELATION_IDS, VALID_SINGLE_PAGE_NUMBERS


@pytest.mark.inttest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_SINGLE_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_single_page(ods_code, page, correlation_id):

    """
    .. include:: ../../partials/happy_path/test_200_get_nhsapp_accounts_single_page.rst
    """
    resp = requests.get(f"{INT_URL}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_200_response_nhsapp_accounts(resp, INT_URL, ods_code, 1)
