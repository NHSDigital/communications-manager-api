"""
Server responds with a 429 when too many requests are raised in a given timeframe
"""
import requests
import pytest


header = {
    "Prefer": "code=429"
}


def __assert_429_error(resp, check_body=True):
    assert resp.status_code == 429

    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_QUOTA"
        assert error.get("status") == "429"
        assert error.get("title") == "Too many requests"
        assert (error.get("description") == "You have made too many requests. "
                                            "Re-send the request after the time (in seconds) "
                                            "specified `Retry-After` header.")


@pytest.mark.smoketest
def test_too_many_requests_get(nhsd_apim_proxy_url, header):
    resp = requests.get(nhsd_apim_proxy_url, headers=header)
    __assert_429_error(resp)


@pytest.mark.smoketest
def test_too_many_requests_post(nhsd_apim_proxy_url, header):
    resp = requests.post(nhsd_apim_proxy_url, headers=header)
    __assert_429_error(resp)


@pytest.mark.smoketest
def test_too_many_requests_put(nhsd_apim_proxy_url, header):
    resp = requests.put(nhsd_apim_proxy_url, headers=header)
    __assert_429_error(resp)


@pytest.mark.smoketest
def test_too_many_requests_patch(nhsd_apim_proxy_url, header):
    resp = requests.patch(nhsd_apim_proxy_url, headers=header)
    __assert_429_error(resp)


@pytest.mark.smoketest
def test_too_many_requests_delete(nhsd_apim_proxy_url, header):
    resp = requests.delete(nhsd_apim_proxy_url, headers=header)
    __assert_429_error(resp)


@pytest.mark.smoketest
def test_too_many_requests_head(nhsd_apim_proxy_url, header):
    resp = requests.head(nhsd_apim_proxy_url, headers=header)
    __assert_429_error(resp)


@pytest.mark.smoketest
def test_too_many_requests_options(nhsd_apim_proxy_url, header):
    resp = requests.options(nhsd_apim_proxy_url, headers=header)
    __assert_429_error(resp)
