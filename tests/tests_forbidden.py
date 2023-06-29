"""
Server returns a 403 when client is not recognised
"""
import requests
import pytest


FORBIDDEN_TOKEN = {
    "Authorization": "Bearer ClientNotRecognised"
}


def __assert_403_error(resp, check_body=True):
    assert resp.status_code == 403

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
@pytest.mark.nhsd_apim_authorization()
def test_403_forbidden_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.nhsd_apim_sandbox_authorization()
def test_403_forbidden_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.nhsd_apim_authorization()
def test_403_forbidden_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.nhsd_apim_authorization()
def test_403_forbidden_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.nhsd_apim_authorization()
def test_403_forbidden_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.nhsd_apim_authorization()
def test_403_forbidden_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp, check_body=False)


@pytest.mark.sandboxtest
@pytest.mark.nhsd_apim_authorization()
def test_403_forbidden_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers=FORBIDDEN_TOKEN)
    __assert_403_error(resp)
