"""
Tests:
Server responds with a 406 value when accept header values do not match the following:
- application/json
- application/vnd.api+json

Scenarios:
For each request type verify that the following returns a 406:
- No header provided
- application/xml
- image/png
- text/plain
- audio/mpeg
- xyz/abc
"""

import requests
import pytest

HEADER_NAME = ["accept", "ACCEPT", "Accept", "AcCePt"]
HEADER_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]


def __assert_406_error(resp, check_body=True):
    assert resp.status_code == 406

    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_NOT_ACCEPTABLE"
        assert error.get("status") == "406"
        assert error.get("title") == "Not acceptable"
        assert (
            error.get("description") == "This service can only generate application/vnd.api+json or application/json."
        )
        assert error.get("source").get("header") == "Accept"


"""
GET 406 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_406_sandbox_get(nhsd_apim_proxy_url, accept_header_name, accept_header_value, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                      accept_header_name, accept_header_value, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


"""
POST 406 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_406_sandbox_post(nhsd_apim_proxy_url, accept_header_name, accept_header_value, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                       accept_header_name, accept_header_value, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


"""
PUT 406 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_406_sandbox_put(nhsd_apim_proxy_url, accept_header_name, accept_header_value, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                      accept_header_name, accept_header_value, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


"""
PATCH 406 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_406_sandbox_patch(nhsd_apim_proxy_url, accept_header_name, accept_header_value, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                        accept_header_name, accept_header_value, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


"""
DELETE 406 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_406_sandbox_delete(nhsd_apim_proxy_url, accept_header_name, accept_header_value, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                         accept_header_name, accept_header_value, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


"""
HEAD 406 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_406_sandbox_head(nhsd_apim_proxy_url, accept_header_name, accept_header_value, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                       accept_header_name, accept_header_value, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp, check_body=False)


"""
OPTIONS 406 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_406_sandbox_options(nhsd_apim_proxy_url, accept_header_name, accept_header_value, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                          accept_header_name, accept_header_value, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value
    })
    __assert_406_error(resp)
