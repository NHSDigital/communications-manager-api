"""
Server correct CORS headers
"""
import requests
import pytest


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def _assert_cors_response(resp):
    assert resp.status_code == 200
    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Allow-Methods") == "GET, PUT, POST, PATCH, DELETE"
    assert resp.headers.get("Access-Control-Max-Age") == "3628800"
    assert resp.headers.get("Access-Control-Allow-Headers") == "origin, x-requested-with, accept, " \
                                                               "content-type, nhsd-session-urid, " \
                                                               "x-correlation-id, authorization"


@pytest.mark.sandboxtest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options_sandbox(nhsd_apim_proxy_url, method):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    _assert_cors_response(resp)

@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_options_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, method):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    _assert_cors_response(resp)


@pytest.mark.sandboxtest
def test_cors_get_sandbox(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_get_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.sandboxtest
def test_cors_post_sandbox(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Content-Type": "application/json"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_post_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Content-Type": "application/json"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.sandboxtest
def test_cors_put_sandbox(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Content-Type": "application/json"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_put_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Content-Type": "application/json"
    })
    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.sandboxtest
def test_cors_delete_sandbox(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_delete_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"
