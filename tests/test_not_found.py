"""
Server response with 404 when resource at requested URI could not be found

Scenarios:
- Invalid URI
- Invalid Request Type
"""
import requests
import pytest


REQUEST_PATH = ["/v1/ignore/i-dont-exist", "/api/fake-endpoint", "/im-a-teapot", "/v1/message-batches"]


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


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_get(nhsd_apim_proxy_url, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
def test_404__invalid_url_one_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/ignore/i-dont-exist", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
def test_404__invalid_url_two_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}/api/fake-endpoint", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
def test_404__invalid_url_three_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}/im-a-teapot", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_put(nhsd_apim_proxy_url, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_patch(nhsd_apim_proxy_url, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_delete(nhsd_apim_proxy_url, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_head(nhsd_apim_proxy_url, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_error(resp, check_body=False)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_options(nhsd_apim_proxy_url, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_error(resp)
