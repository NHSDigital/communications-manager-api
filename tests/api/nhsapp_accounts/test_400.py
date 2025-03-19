import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    VALID_MULTI_PAGE_NUMBERS, INVALID_ODS_CODES, LIVE_ODS_CODES, INVALID_PAGES
from lib.fixtures import *  # NOSONAR


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
def test_400_missing_ods_code(url, bearer_token, page):
    """
    .. include:: ../partials/invalid_ods_code/test_400_nhsapp_accounts_missing_ods_code.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{NHSAPP_ACCOUNTS_ENDPOINT}",
        headers=headers,
        params={PAGE_PARAM_NAME: page})

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_MISSING_ODS_CODE),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("ods_code", INVALID_ODS_CODES)
def test_400_invalid_ods_code(url, bearer_token, ods_code):

    """
    .. include:: ../partials/invalid_ods_code/test_400_nhsapp_accounts_invalid_ods_code.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{NHSAPP_ACCOUNTS_ENDPOINT}",
        headers=headers,
        params={ODS_CODE_PARAM_NAME: ods_code})

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_INVALID_ODS_CODE),
        None
    )


@pytest.mark.devtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", INVALID_PAGES)
def test_400_invalid_page(url, bearer_token, ods_code, page):

    """
    .. include:: ../partials/invalid_page/test_400_nhsapp_accounts_invalid_page.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = requests.get(
        f"{url}{NHSAPP_ACCOUNTS_ENDPOINT}",
        headers=headers,
        params={
            ODS_CODE_PARAM_NAME: ods_code,
            PAGE_PARAM_NAME: page
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_INVALID_PAGE),
        None
    )
