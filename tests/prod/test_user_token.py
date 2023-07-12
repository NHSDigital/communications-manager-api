import requests
import pytest

REQUEST_PATH = "/v1/message-batches"


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


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
def test_user_token_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.get(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers=nhsd_apim_auth_headers)
    __assert_403_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
def test_user_token_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers=nhsd_apim_auth_headers)
    __assert_403_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
def test_user_token_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.put(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers=nhsd_apim_auth_headers)
    __assert_403_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
def test_user_token_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers=nhsd_apim_auth_headers)
    __assert_403_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
def test_user_token_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers=nhsd_apim_auth_headers)
    __assert_403_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
def test_user_token_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.head(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers=nhsd_apim_auth_headers)
    __assert_403_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization(
    {
        "access": "healthcare_worker",
        "level": "aal3",
        "login_form": {"username": "656005750104"},
    }
)
def test_user_token_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.options(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers=nhsd_apim_auth_headers)
    __assert_403_error(resp)
