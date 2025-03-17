import requests
import pytest
from lib import Assertions, Generators
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, VALID_MULTI_PAGE_NUMBERS, VALID_SINGLE_PAGE_NUMBERS
from lib.fixtures import *  # NOSONAR


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_SINGLE_PAGE_NUMBERS)
def test_single_page(url, bearer_token, ods_code, page):
    """
    .. include:: ../partials/happy_path/test_200_get_nhsapp_accounts_single_page.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{NHSAPP_ACCOUNTS_ENDPOINT}",
        headers=headers,
        params={
            ODS_CODE_PARAM_NAME: ods_code,
            PAGE_PARAM_NAME: page
        })

    Assertions.assert_200_response_nhsapp_accounts(resp, url, ods_code, 1)


@pytest.mark.devtestonly
@pytest.mark.devtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
def test_multi_pages(url, bearer_token, ods_code, page):
    """
    .. include:: ../partials/happy_path/test_200_get_nhsapp_accounts_multi_pages.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{NHSAPP_ACCOUNTS_ENDPOINT}",
        headers=headers,
        params={
            ODS_CODE_PARAM_NAME: ods_code,
            PAGE_PARAM_NAME: page
        })

    self_page_in_response = page if page is not None else 1

    Assertions.assert_200_response_nhsapp_accounts(resp, url, ods_code, self_page_in_response)
