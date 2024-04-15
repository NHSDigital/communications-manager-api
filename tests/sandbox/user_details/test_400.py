import requests
import pytest
from lib import Assertions, Generators
from lib.constants.user_details_paths import USER_DETAILS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    VALID_MULTI_PAGE_NUMBERS, INVALID_ODS_CODES, CORRELATION_IDS


@pytest.mark.sandboxtest
@pytest.mark.parametrize("page", VALID_MULTI_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_400_missing_ods_code(nhsd_apim_proxy_url, page, correlation_id):

    resp = requests.get(f"{nhsd_apim_proxy_url}{USER_DETAILS_ENDPOINT}", headers={
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize("page", INVALID_ODS_CODES)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_400_invalid_ods_code(nhsd_apim_proxy_url, page, correlation_id):

    resp = requests.get(f"{nhsd_apim_proxy_url}{USER_DETAILS_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("queryParam.ods-organisation-code"),
        correlation_id
    )
