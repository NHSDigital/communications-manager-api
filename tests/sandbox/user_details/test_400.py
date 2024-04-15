import requests
import pytest
from lib import Assertions, Generators
from lib.constants.user_details_paths import USER_DETAILS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME

VALID_PAGE_NUMBERS = [None, 1, 2, 3, 4, 5, 6]
CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("page", VALID_PAGE_NUMBERS)
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
