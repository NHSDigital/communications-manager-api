import requests
import pytest
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.nhsapp_accounts_paths import NHSAPP_ACCOUNTS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    VALID_MULTI_PAGE_NUMBERS, INVALID_ODS_CODES, CORRELATION_IDS, LIVE_ODS_CODES, INVALID_PAGES


@pytest.mark.devtest
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_400_missing_ods_code(nhsd_apim_proxy_url, nhsd_apim_auth_headers, page, correlation_id):

    """
    .. include:: ../../partials/invalid_ods_code/test_400_nhsapp_accounts_missing_ods_code.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_MISSING_ODS_CODE),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("ods_code", INVALID_ODS_CODES)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_400_invalid_ods_code(nhsd_apim_proxy_url, nhsd_apim_auth_headers, ods_code, correlation_id):

    """
    .. include:: ../../partials/invalid_ods_code/test_400_nhsapp_accounts_invalid_ods_code.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{NHSAPP_ACCOUNTS_ENDPOINT}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_INVALID_ODS_CODE),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", INVALID_PAGES)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_400_invalid_page(nhsd_apim_proxy_url, nhsd_apim_auth_headers, ods_code, page, correlation_id):

    """
    .. include:: ../../partials/invalid_page/test_400_nhsapp_accounts_invalid_page.rst
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
        400,
        Generators.generate_error(constants.ERROR_NHS_APP_ACCOUNTS_INVALID_PAGE),
        correlation_id
    )
