"""
Server response with 404 when resource at requested URI could not be found

Scenarios:
- Invalid URI
- Invalid Request Type
"""
import requests
import pytest


POST_PATHS = ["/v1/ignore/i-dont-exist", "/api/fake-endpoint", "/im-a-teapot"]
REQUEST_PATH = POST_PATHS + ["/v1/message-batches"]


def __assert_404_error(resp, check_body=True):
    assert resp.status_code == 404

    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_NOT_FOUND"
        assert error.get("status") == "404"
        assert error.get("title") == "Resource not found"
        assert (
            error.get("description") == "The resource at the requested URI was not found."
        )


"""
 GET 404 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize("request_path", REQUEST_PATH)
def test_404_get(nhsd_apim_proxy_url, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
    })
    __assert_404_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_authenticated_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    __assert_404_error(resp)


"""
 POST 404 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', POST_PATHS)
def test_404_post(nhsd_apim_proxy_url, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize("request_path", POST_PATHS)
def test_404_authenticated_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    nhsd_apim_auth_headers["Content-Type"] = "application/vnd.api+json"
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    __assert_404_error(resp)


"""
 PUT 404 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_put(nhsd_apim_proxy_url, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_authenticated_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    nhsd_apim_auth_headers["Content-Type"] = "application/vnd.api+json"
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    __assert_404_error(resp)


"""
 PATCH 404 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_patch(nhsd_apim_proxy_url, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_authenticated_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    nhsd_apim_auth_headers["Content-Type"] = "application/vnd.api+json"
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    __assert_404_error(resp)


"""
 DELETE 404 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_delete(nhsd_apim_proxy_url, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_authenticated_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    nhsd_apim_auth_headers["Content-Type"] = "application/vnd.api+json"
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    __assert_404_error(resp)


"""
 HEAD 404 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_head(nhsd_apim_proxy_url, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_error(resp, check_body=False)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_authenticated_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    __assert_404_error(resp, check_body=False)


"""
 OPTIONS 404 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_options(nhsd_apim_proxy_url, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_authenticated_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    __assert_404_error(resp)
