import requests
import pytest
import uuid

FORBIDDEN_TOKEN = {
    "Authorization": "Bearer ClientNotRecognised"
}


x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"


def __assert_403_error(resp, correlation_id=False, check_body=True):
    assert resp.status_code == 403

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_FORBIDDEN"
        assert error.get("status") == "403"
        assert error.get("title") == "Forbidden"
        assert (
            error.get("description") == "Client not recognised or not yet onboarded."
        )
        assert error.get("source").get("header") == "Authorization"


@pytest.mark.sandboxtest
def test_403_forbidden_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
def test_403_forbidden_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
def test_403_forbidden_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
def test_403_forbidden_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
def test_403_forbidden_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
def test_403_forbidden_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp, check_body=False)


@pytest.mark.sandboxtest
def test_403_forbidden_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
def test_403_forbidden_with_correlation_id_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": x_correlation_id_value})
    __assert_403_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_403_forbidden_with_correlation_id_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": x_correlation_id_value})
    __assert_403_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_403_forbidden_with_correlation_id_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": x_correlation_id_value})
    __assert_403_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_403_forbidden_with_correlation_id_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": x_correlation_id_value})
    __assert_403_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_403_forbidden_with_correlation_id_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": x_correlation_id_value})
    __assert_403_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_403_forbidden_with_correlation_id_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": x_correlation_id_value})
    __assert_403_error(resp, correlation_id=True, check_body=False)


@pytest.mark.sandboxtest
def test_403_forbidden_with_correlation_id_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        **FORBIDDEN_TOKEN,
        "X-Correlation-Id": x_correlation_id_value})
    __assert_403_error(resp, correlation_id=True)
