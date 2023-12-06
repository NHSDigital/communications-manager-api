import requests
import pytest
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT

_invalid_uri_methods = [
    (MESSAGE_BATCHES_ENDPOINT, "GET PUT PATCH DELETE HEAD"),
    (MESSAGES_ENDPOINT, "GET PUT PATCH DELETE HEAD"),
    (f"{MESSAGES_ENDPOINT}/dummy-id", "POST PUT PATCH DELETE")
]

INVALID_URI_METHOD_COMBINATIONS = []
for uri, all_methods_to_test in _invalid_uri_methods:
    for method in all_methods_to_test.split():
        INVALID_URI_METHOD_COMBINATIONS.append((uri, method))


@pytest.mark.sandboxtest
@pytest.mark.parametrize('uri, method', INVALID_URI_METHOD_COMBINATIONS)
def test_405_message_batch_invalid_method(nhsd_apim_proxy_url, uri, method):
    """
    .. include:: ../../partials/not_allowed/test_405_not_allowed.rst
    """
    data = Generators.generate_valid_create_message_body("sandbox")
    resp = requests.request(
        method,
        f"{nhsd_apim_proxy_url}/{uri}",
        headers={
            "Content-Type": "application/json"
        },
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        405,
        Generators.generate_not_allowed_error() if method != 'HEAD' else None,
        None
    )
