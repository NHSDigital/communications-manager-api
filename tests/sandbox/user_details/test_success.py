import requests
import pytest
from lib import Assertions, Generators
from lib.constants.user_details_paths import USER_DETAILS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    SINGLE_PAGE_ODS_CODES, MULTIPLE_PAGES_ODS_CODES

VALID_MULTI_PAGE_NUMBERS = [None, 1, 2, 3, 4, 5, 6, 7, 8]
MULTI_LAST_PAGE = 8
VALID_SINGLE_PAGE_NUMBERS = [None, 1]
CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("ods_code", SINGLE_PAGE_ODS_CODES)
@pytest.mark.parametrize("page", VALID_SINGLE_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_single_page(nhsd_apim_proxy_url, ods_code, page, correlation_id):

    resp = requests.get(f"{nhsd_apim_proxy_url}{USER_DETAILS_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_200_response_nhs_app_accounts(resp, nhsd_apim_proxy_url, ods_code, 1, None, 1)


@pytest.mark.sandboxtest
@pytest.mark.parametrize("ods_code", MULTIPLE_PAGES_ODS_CODES)
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_multi_pages(nhsd_apim_proxy_url, ods_code, page, correlation_id):

    resp = requests.get(f"{nhsd_apim_proxy_url}{USER_DETAILS_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    self_page_in_response = page if page is not None else 1
    next_page_in_response = page + 1 if page < MULTI_LAST_PAGE else None

    Assertions.assert_200_response_nhs_app_accounts(resp, nhsd_apim_proxy_url, ods_code, self_page_in_response,
                                                    next_page_in_response, 8)
