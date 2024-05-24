import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants.constants import INT_URL
from lib.constants.user_details_paths import USER_DETAILS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    LIVE_ODS_CODES, CORRELATION_IDS, INVALID_ODS_CODES

INVALID_PAGE_NUMBERS = [1000, 2000, 3000]


@pytest.mark.inttest
@pytest.mark.parametrize("ods_code", LIVE_ODS_CODES)
@pytest.mark.parametrize("page", INVALID_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_404_page_not_found(ods_code, page, correlation_id):

    """
    .. include:: ../../partials/not_found/test_404_nhs_accounts_page_not_found.rst
    """
    resp = requests.get(f"{INT_URL}{USER_DETAILS_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        correlation_id
    )

@pytest.mark.inttest
@pytest.mark.parametrize("ods_code", INVALID_ODS_CODES)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_404_invalid_ods_code(ods_code, correlation_id):

    """
    .. include:: ../../partials/not_found/test_404_nhs_accounts_invalid_ods_code.rst
    """
    resp = requests.get(f"{INT_URL}{USER_DETAILS_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.Generators.generate_not_found_error(),
        correlation_id
    )

    