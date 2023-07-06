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
@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options(nhsd_apim_proxy_url, method):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })

    _assert_cors_response(resp)


@pytest.mark.sandboxtest
@pytest.mark.prodtest
def test_cors_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.sandboxtest
@pytest.mark.prodtest
def test_cors_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Content-Type": "application/json"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.sandboxtest
@pytest.mark.prodtest
def test_cors_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Content-Type": "application/json"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"


@pytest.mark.sandboxtest
@pytest.mark.prodtest
def test_cors_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers={
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    assert resp.headers.get("Access-Control-Allow-Origin") == "https://my.website"
    assert resp.headers.get("Access-Control-Expose-Headers") == "x-correlation-id"
