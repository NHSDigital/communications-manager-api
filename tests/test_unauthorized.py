"""
Server returns a 401 when access token missing invalid or expired

Scenarios
- Invalid
- Missing
"""
import requests
import pytest

MOCK_TOKEN = {
    "Authorization": "Bearer InvalidMockToken"
}
INVALID_TOKEN = ["Bearer xyzcba", "Bearer", "junk"]


def __assert_401_error(resp, check_body=True):
    assert resp.status_code == 401

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
def test_401_invalid_sandbox_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp, check_body=False)


@pytest.mark.sandboxtest
def test_401_invalid_sandbox_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers=MOCK_TOKEN)
    __assert_401_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_401_invalid_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_401_invalid_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_401_invalid_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_401_invalid_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_401_invalid_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_401_invalid_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_401_invalid_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers=nhsd_apim_auth_headers)
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
def test_401_missing_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}")
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
def test_401_missing_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}")
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
def test_401_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}")
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
def test_401_missing_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}")
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
def test_401_missing_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}")
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
def test_401_missing_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}")
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', INVALID_TOKEN)
def test_401_invalid_prod_get(nhsd_apim_proxy_url, invalid_token):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={"Authorization": invalid_token})
    __assert_401_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', INVALID_TOKEN)
def test_401_invalid_prod_post(nhsd_apim_proxy_url, invalid_token):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers={"Authorization": invalid_token})
    __assert_401_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', INVALID_TOKEN)
def test_401_invalid_prod_put(nhsd_apim_proxy_url, invalid_token):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers={"Authorization": invalid_token})
    __assert_401_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', INVALID_TOKEN)
def test_401_invalid_prod_patch(nhsd_apim_proxy_url, invalid_token):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers={"Authorization": invalid_token})
    __assert_401_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', INVALID_TOKEN)
def test_401_invalid_prod_delete(nhsd_apim_proxy_url, invalid_token):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers={"Authorization": invalid_token})
    __assert_401_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', INVALID_TOKEN)
def test_401_invalid_prod_head(nhsd_apim_proxy_url, invalid_token):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers={"Authorization": invalid_token})
    __assert_401_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.parametrize('invalid_token', INVALID_TOKEN)
def test_401_invalid_prod_options(nhsd_apim_proxy_url, invalid_token):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={"Authorization": invalid_token})
    __assert_401_error(resp)
