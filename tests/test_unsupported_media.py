"""
Server responds with a 415 status code when content type does not match
- application/json
- application/vnd.api+json

This error affects the following request types:
- Post
- Patch
- Put
"""
import requests
import pytest
import uuid


CONTENT_TYPE_NAME = ["content-type", "CONTENT_TYPE", "Content_Type", "conTENT_tYpe"]
CONTENT_TYPE_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]
x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"


def __assert_415_error(resp, correlation_id=False):
    assert resp.status_code == 415

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    error = resp.json().get("errors")[0]
    assert error.get("id") == "CM_UNSUPPORTED_MEDIA"
    assert error.get("status") == "415"
    assert error.get("title") == "Unsupported media"
    assert error.get("source").get("header") == "Content-Type"
    assert error.get("description") == "Invalid content-type, this API only " \
                                       "supports application/vnd.api+json or " \
                                       "application/json."


"""
 POST 415 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_sandbox_post(nhsd_apim_proxy_url, content_type_name, content_type_value, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "application/json",
        content_type_name: content_type_value
    })
    __assert_415_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_prod_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                       content_type_name, content_type_value, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        content_type_name: content_type_value
    })
    __assert_415_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_sandbox_with_correlation_id_post(nhsd_apim_proxy_url, content_type_name,
                                              content_type_value, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_415_error(resp, correlation_id=True)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_prod_with_correlation_id_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                           content_type_name, content_type_value, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_415_error(resp, correlation_id=True)


"""
 PUT 415 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_sandbox_put(nhsd_apim_proxy_url, content_type_name, content_type_value, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "application/json",
        content_type_name: content_type_value
    })
    __assert_415_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_prod_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                      content_type_name, content_type_value, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        content_type_name: content_type_value
    })
    __assert_415_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_sandbox_with_correlation_id_put(nhsd_apim_proxy_url, content_type_name,
                                             content_type_value, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_415_error(resp, correlation_id=True)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_prod_with_correlation_id_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                          content_type_name, content_type_value, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_415_error(resp, correlation_id=True)


"""
 PATCH 415 tests
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_sandbox_patch(nhsd_apim_proxy_url, content_type_name,
                           content_type_value, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "application/json",
        content_type_name: content_type_value
    })
    __assert_415_error(resp)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_prod_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                        content_type_name, content_type_value, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        content_type_name: content_type_value
    })
    __assert_415_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_sandbox_with_correlation_id_patch(nhsd_apim_proxy_url, content_type_name,
                                               content_type_value, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_415_error(resp, correlation_id=True)


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('content_type_name', CONTENT_TYPE_NAME)
@pytest.mark.parametrize('content_type_value', CONTENT_TYPE_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_415_prod_with_correlation_id_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                            content_type_name, content_type_value, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        content_type_name: content_type_value,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_415_error(resp, correlation_id=True)
