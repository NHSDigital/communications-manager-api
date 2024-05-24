import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants.constants import INT_URL
from lib.constants.user_details_paths import USER_DETAILS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    VALID_MULTI_PAGE_NUMBERS, CORRELATION_IDS


@pytest.mark.inttest
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_400_missing_ods_code(page, correlation_id):

    """
    .. include:: ../../partials/invalid_ods_code/test_400_nhs_accounts_missing_ods_code.rst
    """
    resp = requests.get(f"{INT_URL}{USER_DETAILS_ENDPOINT}", headers={
        "Authorization": Authentication.generate_authentication("int"),
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_missing_value_error("queryParam.ods-organisation-code"),
        correlation_id
    )



