import requests
import pytest
import uuid

HEADER_NAME = ["accept", "ACCEPT", "Accept", "AcCePt"]
HEADER_VALUE = ["", "application/xml", "image/png", "text/plain", "audio/mpeg", "xyz/abc"]
REQUEST_PATH = ["/v1/ignore", "/api/ignore"]
x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"


def __assert_406_error(resp, correlation_id=False, check_body=True):
    assert resp.status_code == 406

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_NOT_ACCEPTABLE"
        assert error.get("status") == "406"
        assert error.get("title") == "Not acceptable"
        assert (
            error.get("description") == "This service can only generate application/vnd.api+json or application/json."
        )
        assert error.get("source").get("header") == "Accept"


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


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_with_correlation_id_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                          accept_header_name, accept_header_value, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_406_error(resp, correlation_id=True)


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


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_with_correlation_id_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                           accept_header_name, accept_header_value, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-id": x_correlation_id_value
    })
    __assert_406_error(resp, correlation_id=True)


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


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_with_correlation_id_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                          accept_header_name, accept_header_value, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-id": x_correlation_id_value
    })
    __assert_406_error(resp, correlation_id=True)


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


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_with_correlation_id_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                            accept_header_name, accept_header_value, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-id": x_correlation_id_value
    })
    __assert_406_error(resp, correlation_id=True)


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


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_with_correlation_id_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                             accept_header_name, accept_header_value, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-id": x_correlation_id_value
    })
    __assert_406_error(resp, correlation_id=True)


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


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_with_correlation_id_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                           accept_header_name, accept_header_value, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-id": x_correlation_id_value
    })
    __assert_406_error(resp, correlation_id=True, check_body=False)


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


@pytest.mark.prodtest
@pytest.mark.parametrize('accept_header_name', HEADER_NAME)
@pytest.mark.parametrize('accept_header_value', HEADER_VALUE)
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_406_prod_with_correlation_id_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers,
                                              accept_header_name, accept_header_value, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}/{request_path}", headers={
        **nhsd_apim_auth_headers,
        accept_header_name: accept_header_value,
        "X-Correlation-id": x_correlation_id_value
    })
    __assert_406_error(resp, correlation_id=True)
