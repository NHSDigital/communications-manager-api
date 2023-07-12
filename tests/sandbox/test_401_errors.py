import requests
import pytest
import uuid

MOCK_TOKEN = {
    "Authorization": "Bearer InvalidMockToken"
}
x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"


def __assert_401_error(resp, correlation_id=False, check_body=True):
    assert resp.status_code == 401

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_DENIED"
        assert error.get("status") == "401"
        assert error.get("title") == "Access denied"
        assert error.get("description") == "Access token missing, invalid or expired, " \
                                           "or calling application not configured for " \
                                           "this operation."
        assert error.get("source").get("header") == "Authorization"


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_with_correlation_id_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_401_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_with_correlation_id_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_401_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_with_correlation_id_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_401_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_with_correlation_id_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_401_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_with_correlation_id_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_401_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp, check_body=False)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_with_correlation_id_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_401_error(resp, correlation_id=True, check_body=False)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_with_correlation_id_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_401_error(resp, correlation_id=True)
