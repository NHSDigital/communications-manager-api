import requests
import pytest
from lib import Assertions, Generators
from lib.constants.constants import PROD_URL
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, CORRELATION_IDS, VALID_MULTI_PAGE_NUMBERS, \
    MULTI_LAST_PAGE, VALID_SINGLE_PAGE_NUMBERS
from lib.fixtures import *


@pytest.mark.prodtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_SINGLE_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_single_page(bearer_token_prod, ods_code, page, correlation_id):

    """
    .. include:: ../../partials/happy_path/test_200_get_nhsapp_accounts_single_page.rst
    """
    resp = requests.get(f"{PROD_URL}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        "Authorization": bearer_token_prod,
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_200_response_nhsapp_accounts(resp, PROD_URL, ods_code, 1)


@pytest.mark.prodtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_multi_pages(bearer_token_prod, ods_code, page, correlation_id):

    """
    .. include:: ../../partials/happy_path/test_200_get_nhsapp_accounts_multi_pages.rst
    """
    resp = requests.get(f"{PROD_URL}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        "Authorization": bearer_token_prod,
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    self_page_in_response = page if page is not None else 1

    Assertions.assert_200_response_nhsapp_accounts(resp, PROD_URL, ods_code, self_page_in_response)
