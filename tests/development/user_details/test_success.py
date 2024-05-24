import requests
import pytest
from lib import Assertions, Generators
from lib.constants.user_details_paths import USER_DETAILS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, CORRELATION_IDS, VALID_MULTI_PAGE_NUMBERS, \
    MULTI_LAST_PAGE, VALID_SINGLE_PAGE_NUMBERS


@pytest.mark.devtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_SINGLE_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_single_page(nhsd_apim_proxy_url, nhsd_apim_auth_headers, ods_code, page, correlation_id):

    """
    .. include:: ../../partials/happy_path/test_200_get_nhs_app_accounts_single_page.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{USER_DETAILS_ENDPOINT}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_200_response_nhs_app_accounts(resp, nhsd_apim_proxy_url, ods_code, 1)


@pytest.mark.devtest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_multi_pages(nhsd_apim_proxy_url, nhsd_apim_auth_headers, ods_code, page, correlation_id):

    """
    .. include:: ../../partials/happy_path/test_200_get_nhs_app_accounts_multi_pages.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}{USER_DETAILS_ENDPOINT}", headers={
        **nhsd_apim_auth_headers,
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    self_page_in_response = page if page is not None else 1

    Assertions.assert_200_response_nhs_app_accounts(resp, nhsd_apim_proxy_url, ods_code, self_page_in_response)