"""
See
https://github.com/NHSDigital/pytest-nhsd-apim/blob/main/tests/test_examples.py
for more ideas on how to test the authorization of your API.
"""
import requests
import pytest
import time
from os import getenv


def _determine_expected_commitId(deployed_commitId):
    expected_commitId = getenv('SOURCE_COMMIT_ID')
    if expected_commitId is None or expected_commitId == "":
        return deployed_commitId

    return expected_commitId


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_ping(nhsd_apim_proxy_url):
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    assert resp.status_code == 200


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_wait_for_ping(nhsd_apim_proxy_url):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    deployed_commitId = resp.json().get("commitId")

    while (deployed_commitId != _determine_expected_commitId(deployed_commitId)
            and retries <= 30
            and resp.status_code == 200):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
        deployed_commitId = resp.json().get("commitId")
        time.sleep(1)
        retries += 1

    if resp.status_code == 429:
        raise AssertionError('Unexpected 429')

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")

    assert deployed_commitId == _determine_expected_commitId(deployed_commitId)


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers
    )

    if resp.status_code == 429:
        raise AssertionError('Unexpected 429')

    assert resp.status_code == 200


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_401_status_without_apikey(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status"
    )

    if resp.status_code == 429:
        raise AssertionError('Unexpected 429')

    assert resp.status_code == 401


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_wait_for_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
    deployed_commitId = resp.json().get("commitId")

    while (deployed_commitId != _determine_expected_commitId(deployed_commitId)
            and retries <= 30
            and resp.status_code == 200
            and resp.json().get("version")):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
        deployed_commitId = resp.json().get("commitId")
        time.sleep(1)
        retries += 1

    if resp.status_code == 429:
        raise AssertionError('Unexpected 429')

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")
    elif not resp.json().get("version"):
        pytest.fail("version not found")

    assert deployed_commitId == _determine_expected_commitId(deployed_commitId)
