import requests
import pytest
import uuid


REQUEST_PATH = ""
x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"


def __assert_408_error(resp, correlation_id=False, check_body=True):
    assert resp.status_code == 408

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_TIMEOUT"
        assert error.get("status") == "408"
        assert error.get("title") == "Request timeout"
        assert (
            error.get("description") == "The service was unable to receive your request within the timeout period."
        )


def __assert_504_error(resp, correlation_id=False, check_body=True):
    assert resp.status_code == 504

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_TIMEOUT"
        assert error.get("status") == "504"
        assert error.get("title") == "Unable to call service"
        assert (
            error.get("description") == "The downstream service has not responded within the configured timeout period."
        )


@pytest.mark.sandboxtest
def test_408_timeout_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout_408")
    __assert_408_error(resp)


@pytest.mark.sandboxtest
def test_504_timeout_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout_504")
    __assert_504_error(resp)


@pytest.mark.sandboxtest
def test_504_timeout_simulate(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout?sleep=3000")
    __assert_504_error(resp)


@pytest.mark.sandboxtest
def test_408_timeout_with_correlation_id_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout_408", headers={
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_408_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_504_timeout_with_correlation_id_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout_504", headers={
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_504_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_504_timeout_with_correlation_id_simulate(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout?sleep=3000", headers={
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_504_error(resp, correlation_id=True)
