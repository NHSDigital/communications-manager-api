import requests
import pytest


ACCEPT_HEADERS = [
    {
        "headers": {
            "Accept": "application/vnd.api+json"
        },
        "expect": "application/vnd.api+json"
    },
    {
        "headers": {
            "Accept": "*/*"
        },
        "expect": "application/vnd.api+json"
    },
    {
        "headers": {
            "Accept": "application/json"
        },
        "expect": "application/json"
    }
]


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_authenticated_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_authenticated_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_authenticated_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_authenticated_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_authenticated_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_authenticated_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_authenticated_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        **accept_headers.get("headers")
    })
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
