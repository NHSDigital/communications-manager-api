"""
System returns an x-correlation-id header if one is provided
"""
import requests
import pytest
import uuid


x_correlation_id_value = f"0{str(uuid.uuid1())[1:]}"
REQUEST_PATH = ["", "/", "/api/v1/send", "/v1/message-batches", "/v1/message-batches/"]

"""
GET x-correlation-id
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_sandbox_get(nhsd_apim_proxy_url, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_with_x_correlation_id_prod_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value,
        **nhsd_apim_auth_headers})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_sandbox_get(nhsd_apim_proxy_url, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.prodtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_without_x_correlation_id_prod_get(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    assert resp.headers.get("x-correlation-id") is None


"""
POST x-correlation-id
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_sandbox_post(nhsd_apim_proxy_url, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_prod_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value,
        **nhsd_apim_auth_headers})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_sandbox_post(nhsd_apim_proxy_url, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_prod_post(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    assert resp.headers.get("x-correlation-id") is None


"""
PUT x-correlation-id
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_sandbox_put(nhsd_apim_proxy_url, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_prod_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value,
        **nhsd_apim_auth_headers})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_sandbox_put(nhsd_apim_proxy_url, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_prod_put(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    assert resp.headers.get("x-correlation-id") is None


"""
PATCH x-correlation-id
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_sandbox_patch(nhsd_apim_proxy_url, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_prod_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value,
        **nhsd_apim_auth_headers})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_sandbox_patch(nhsd_apim_proxy_url, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_prod_patch(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    assert resp.headers.get("x-correlation-id") is None


"""
DELETE x-correlation-id
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_sandbox_delete(nhsd_apim_proxy_url, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_prod_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value,
        **nhsd_apim_auth_headers})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_sandbox_delete(nhsd_apim_proxy_url, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_prod_delete(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    assert resp.headers.get("x-correlation-id") is None


"""
HEAD x-correlation-id
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_sandbox_head(nhsd_apim_proxy_url, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_prod_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value,
        **nhsd_apim_auth_headers})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_sandbox_head(nhsd_apim_proxy_url, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_prod_head(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    assert resp.headers.get("x-correlation-id") is None


"""
OPTIONS x-correlation-id
"""


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_sandbox_options(nhsd_apim_proxy_url, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_with_x_correlation_id_prod_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "x-correlation-id": x_correlation_id_value,
        **nhsd_apim_auth_headers})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_sandbox_options(nhsd_apim_proxy_url, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_request_without_x_correlation_id_prod_options(nhsd_apim_proxy_url, nhsd_apim_auth_headers, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers=nhsd_apim_auth_headers)
    assert resp.headers.get("x-correlation-id") is None
