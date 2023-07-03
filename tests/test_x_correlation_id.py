"""
System returns an x-correlation-id header if one is provided
"""
import requests
import pytest
import uuid


x_correlation_id_value = f"0{str(uuid.uuid1())[1:]}"


@pytest.mark.sandboxtest
def test_request_with_x_correlation_id_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
def test_request_with_x_correlation_id_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
def test_request_with_x_correlation_id_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
def test_request_with_x_correlation_id_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
def test_request_with_x_correlation_id_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
def test_request_with_x_correlation_id_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
def test_request_with_x_correlation_id_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "x-correlation-id": x_correlation_id_value})
    assert resp.headers.get("x-correlation-id") == x_correlation_id_value


@pytest.mark.sandboxtest
def test_request_without_x_correlation_id_get(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/v1/message-batches")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.sandboxtest
def test_request_without_x_correlation_id_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.sandboxtest
def test_request_without_x_correlation_id_put(nhsd_apim_proxy_url):
    resp = requests.put(f"{nhsd_apim_proxy_url}/v1/message-batches")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.sandboxtest
def test_request_without_x_correlation_id_patch(nhsd_apim_proxy_url):
    resp = requests.patch(f"{nhsd_apim_proxy_url}/v1/message-batches")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.sandboxtest
def test_request_without_x_correlation_id_delete(nhsd_apim_proxy_url):
    resp = requests.delete(f"{nhsd_apim_proxy_url}/v1/message-batches")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.sandboxtest
def test_request_without_x_correlation_id_head(nhsd_apim_proxy_url):
    resp = requests.head(f"{nhsd_apim_proxy_url}/v1/message-batches")
    assert resp.headers.get("x-correlation-id") is None


@pytest.mark.sandboxtest
def test_request_without_x_correlation_id_options(nhsd_apim_proxy_url):
    resp = requests.options(f"{nhsd_apim_proxy_url}/v1/message-batches")
    assert resp.headers.get("x-correlation-id") is None
