import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
import time

test_client_1_details = {
    "email": "ian.hodges1@nhs.net",
    "name": "NHS Notify Test Client 1"
}


def default_request_url(url):
    return f"{url}{MESSAGES_ENDPOINT}/pending_enrichment_request_item_id"


def send_multiple_requests(url, headers, count=10, delay=0):
    for _ in range(count):
        resp = requests.get(url, headers=headers)
        if delay > 0:
            time.sleep(delay)
    return resp


@pytest.mark.devperftest
def test_429_triggered_app_quota(url, bearer_token, rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_429_global_app_quota.rst
    """
    rate_limiting.set_rate_limit(app_quota=4)
    headers = Generators.generate_valid_headers(bearer_token.value)
    resp = send_multiple_requests(default_request_url(url), headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error_custom(
            "Your application, Comms-manager-local, "
            "has exceeded its quota of 4 requests every 1 minute(s) and is being rate limited."),
        None
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "60"


@pytest.mark.devperftest
def test_429_triggered_app_spikearrest(url, bearer_token, rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_429_global_app_spikearrest.rst
    """
    rate_limiting.set_rate_limit(app_spikearrest="4pm")
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = send_multiple_requests(default_request_url(url), headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error_custom(
            "Your application, Comms-manager-local, "
            "has created a spike in traffic and is being rate limited. Please reduce the frequency of your requests."),
        None
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "1"


@pytest.mark.devperftest
def test_429_triggered_proxy_quota(url, bearer_token, rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_429_proxy_quota.rst
    """
    rate_limiting.set_rate_limit(proxy_quota=4)
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = send_multiple_requests(default_request_url(url), headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error_custom(
            "This API is currently receiving a high volume of requests "
            "and is being rate limited."),
        None
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "60"


@pytest.mark.devperftest
def test_429_triggered_proxy_spikearrest(url, bearer_token, rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_429_proxy_spikearrest.rst
    """
    rate_limiting.set_rate_limit(proxy_spikearrest="4pm")
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = send_multiple_requests(default_request_url(url), headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error_custom(
            "This API is currently receiving a high volume of requests "
            "and is being rate limited."),
        None
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "1"


@pytest.mark.devperftest
def test_429_triggered_specific_app_quota(url, bearer_token_internal_dev_test_1, rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_429_specific_app_quota.rst
    """
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], quota=4)
    headers = Generators.generate_valid_headers(bearer_token_internal_dev_test_1.value)

    resp = send_multiple_requests(default_request_url(url), headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error_custom(
            "Your application, NHS Notify Test Client 1, "
            "has exceeded its quota of 4 requests every 1 minute(s) and is being rate limited."),
        None
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "60"


@pytest.mark.devperftest
def test_429_not_triggered_other_specific_app_quota(url, bearer_token, rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_200_specific_app_quota_different_app.rst
    """
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], quota=4)
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = send_multiple_requests(default_request_url(url), headers)

    assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"


@pytest.mark.devperftest
def test_429_triggered_specific_app_spikearrest(url,
                                                bearer_token,
                                                bearer_token_internal_dev_test_1,
                                                rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_429_specific_app_spikearrest.rst
    """
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], spikearrest="4pm")
    headers = Generators.generate_valid_headers(bearer_token_internal_dev_test_1.value)

    resp = send_multiple_requests(default_request_url(url), headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error_custom(
            "Your application, NHS Notify Test Client 1, "
            "has created a spike in traffic and is being rate limited. Please reduce the frequency of your requests."),
        None
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "1"


@pytest.mark.devperftest
def test_429_not_triggered_other_specific_spikearrest(url, bearer_token, rate_limiting):

    """
    .. include:: ../partials/too_many_requests/test_200_specific_app_spikearrest_different_app.rst
    """
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], spikearrest="4pm")
    headers = Generators.generate_valid_headers(bearer_token.value)

    resp = send_multiple_requests(default_request_url(url), headers)

    assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
