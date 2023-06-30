"""
Server will respond with a Content-Type appropriate to the request sent

Response Content-Type will be application/vnd.api+json when:
- Accept Header is Invalid (415) - incorporated into test_unsupported_media.py
- Accept Header allows any content type (*/*)
- Accept Header is application/vnd.api+json

Response Content-Type will be application/json when acceot header is application/json
"""

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


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_get(nhsd_apim_proxy_url, accept_headers):
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_post(nhsd_apim_proxy_url, accept_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_put(nhsd_apim_proxy_url, accept_headers):
    resp = requests.put(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_patch(nhsd_apim_proxy_url, accept_headers):
    resp = requests.patch(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_delete(nhsd_apim_proxy_url, accept_headers):
    resp = requests.delete(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_head(nhsd_apim_proxy_url, accept_headers):
    resp = requests.head(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', ACCEPT_HEADERS)
def test_application_response_type_options(nhsd_apim_proxy_url, accept_headers):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers=accept_headers.get("headers"))
    assert resp.headers.get("Content-Type") == accept_headers.get("expect")
