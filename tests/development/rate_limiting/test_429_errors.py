import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
import time

CORRELATION_IDS = [None, "0f160ae2-9b62-47bf-bdf0-c6a844d59488"]

test_client_1_details = {
    "email": "ian.hodges1@nhs.net",
    "name": "NHS Notify Test Client 1"
}


def default_request_url(nhsd_apim_proxy_url):
    return f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/pending_enrichment_request_item_id"


def send_multiple_requests(url, headers, count=10, delay=0):
    for i in range(count):
        resp = requests.get(url, headers=headers)
        if delay > 0:
            time.sleep(delay)
    return resp


@pytest.mark.devperftest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_429_triggered_app_quota(nhsd_apim_proxy_url, bearer_token_internal_dev, rate_limiting, correlation_id):
    rate_limiting.set_rate_limit(app_quota=4)

    headers = {
        "Authorization": bearer_token_internal_dev.value,
        "Accept": "*/*",
        "Content-Type": "application/json",
        "X-Correlation-Id": correlation_id
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        429,
        Generators.generate_quota_error_custom(
            "Your application, Comms-manager-local, "
            "has exceeded its quota of 4 requests every 1 minute(s) and is being rate limited."),
        correlation_id
    )

    assert "Retry-After" in resp.headers
    assert resp.headers.get("Retry-After") == "60"


@pytest.mark.devperftest
def test_429_triggered_app_spikearrest(nhsd_apim_proxy_url, bearer_token_internal_dev, rate_limiting):
    rate_limiting.set_rate_limit(app_spikearrest="4pm")

    headers = {
        "Authorization": bearer_token_internal_dev.value,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

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
def test_429_triggered_proxy_quota(nhsd_apim_proxy_url, bearer_token_internal_dev, rate_limiting):
    rate_limiting.set_rate_limit(proxy_quota=4)

    headers = {
        "Authorization": bearer_token_internal_dev.value,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

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
def test_429_triggered_proxy_spikearrest(nhsd_apim_proxy_url, bearer_token_internal_dev, rate_limiting):
    rate_limiting.set_rate_limit(proxy_spikearrest="4pm")

    headers = {
        "Authorization": bearer_token_internal_dev.value,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

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
def test_429_triggered_specific_app_quota(nhsd_apim_proxy_url, bearer_token_internal_dev_test_1, rate_limiting):
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], quota=4)

    headers = {
        "Authorization": bearer_token_internal_dev_test_1.value,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

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
def test_429_not_triggered_other_specific_app_quota(nhsd_apim_proxy_url, bearer_token_internal_dev, rate_limiting):
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], quota=4)

    headers = {
        "Authorization": bearer_token_internal_dev.value,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

    assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"


@pytest.mark.devperftest
def test_429_triggered_specific_app_spikearrest(nhsd_apim_proxy_url,
                                                bearer_token_internal_dev,
                                                bearer_token_internal_dev_test_1,
                                                rate_limiting):
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], spikearrest="4pm")

    headers = {
        "Authorization": bearer_token_internal_dev_test_1.value,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

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
def test_429_not_triggered_other_specific_spikearrest(nhsd_apim_proxy_url, bearer_token_internal_dev, rate_limiting):
    rate_limiting.set_default_rate_limit()
    rate_limiting.set_app_ratelimit(test_client_1_details["email"], test_client_1_details["name"], spikearrest="4pm")

    headers = {
        "Authorization": bearer_token_internal_dev.value,
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    resp = send_multiple_requests(default_request_url(nhsd_apim_proxy_url), headers)

    assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
