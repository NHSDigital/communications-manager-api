import pytest
import requests


HEADERS = {"Prefer": "code=503"}


def __assert_503_error(resp, check_body=True):
    assert resp.status_code == 503

    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_SERVICE_UNAVAILABLE"
        assert error.get("status") == "503"
        assert error.get("title") == "The service is currently unavailable"
        assert error.get("description") == "The service is currently not able to "\
            "process this request, try again later."


@pytest.mark.sandboxtest
def test_service_unavailable_get(nhsd_apim_proxy_url):
    resp = requests.get(nhsd_apim_proxy_url, headers=HEADERS)
    __assert_503_error(resp)


@pytest.mark.sandboxtest
def test_service_unavailable_post(nhsd_apim_proxy_url):
    resp = requests.post(nhsd_apim_proxy_url, headers=HEADERS)
    __assert_503_error(resp)


@pytest.mark.sandboxtest
def test_service_unavailable_put(nhsd_apim_proxy_url):
    resp = requests.put(nhsd_apim_proxy_url, headers=HEADERS)
    __assert_503_error(resp)


@pytest.mark.sandboxtest
def test_service_unavailable_patch(nhsd_apim_proxy_url):
    resp = requests.patch(nhsd_apim_proxy_url, headers=HEADERS)
    __assert_503_error(resp)


@pytest.mark.sandboxtest
def test_service_unavailable_delete(nhsd_apim_proxy_url):
    resp = requests.delete(nhsd_apim_proxy_url, headers=HEADERS)
    __assert_503_error(resp)


@pytest.mark.sandboxtest
def test_service_unavailable_head(nhsd_apim_proxy_url):
    resp = requests.head(nhsd_apim_proxy_url, headers=HEADERS)
    __assert_503_error(resp, check_body=False)


@pytest.mark.sandboxtest
def test_service_unavailable_options(nhsd_apim_proxy_url):
    resp = requests.options(nhsd_apim_proxy_url, headers=HEADERS)
    __assert_503_error(resp)
