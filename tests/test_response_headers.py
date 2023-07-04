import requests
import pytest


expected_access_control_headers = [
    "origin", "x-requested-with", "accept", "content-type", "nhsd-session-urid", "x-correlation-id"]
expected_access_control_methods = ["GET", "POST", "PUT", "DELETE"]


@pytest.mark.sandboxtest
def test_options_200_response_headers(nhsd_apim_proxy_url):
    resp = requests.options(nhsd_apim_proxy_url, headers={
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": "POST"
    })
    assert resp.status_code == 200
    response = resp.headers
    assert "https://my.website" in response.get("Access-Control-Allow-Origin")
    for value in expected_access_control_headers:
        assert value in response.get("Access-Control-Allow-Headers")
    for value in expected_access_control_methods:
        assert value in response.get("Access-Control-Allow-Methods")
