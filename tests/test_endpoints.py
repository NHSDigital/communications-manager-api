"""
See
https://github.com/NHSDigital/pytest-nhsd-apim/blob/main/tests/test_examples.py
for more ideas on how to test the authorization of your API.
"""
import requests
import pytest
import time
from os import getenv
from lib.constants import UNEXPECTED_429


def determine_expected_commit_id(deployed_commit_id):
    expected_commit_id = getenv('SOURCE_COMMIT_ID')
    if expected_commit_id is None or expected_commit_id == "":
        return deployed_commit_id

    return expected_commit_id


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
    deployed_commit_id = resp.json().get("commitId")

    while (deployed_commit_id != determine_expected_commit_id(deployed_commit_id)
            and retries <= 30
            and resp.status_code == 200):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
        deployed_commit_id = resp.json().get("commitId")
        time.sleep(5)
        retries += 1

    if resp.status_code == 429:
        raise UNEXPECTED_429

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")

    assert deployed_commit_id == determine_expected_commit_id(deployed_commit_id)


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers
    )

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.status_code == 200


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_401_status_without_apikey(nhsd_apim_proxy_url):
    resp = requests.get(
        f"{nhsd_apim_proxy_url}/_status"
    )

    if resp.status_code == 429:
        raise UNEXPECTED_429

    assert resp.status_code == 401


@pytest.mark.smoketest
@pytest.mark.sandboxtest
@pytest.mark.devtest
def test_wait_for_status(nhsd_apim_proxy_url, status_endpoint_auth_headers):
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
    deployed_commit_id = resp.json().get("commitId")

    while (deployed_commit_id != determine_expected_commit_id(deployed_commit_id)
            and retries <= 30
            and resp.status_code == 200
            and resp.json().get("version")):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_status", headers=status_endpoint_auth_headers)
        deployed_commit_id = resp.json().get("commitId")
        time.sleep(5)
        retries += 1

    if resp.status_code == 429:
        raise UNEXPECTED_429

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")
    elif not resp.json().get("version"):
        pytest.fail("version not found")

    assert deployed_commit_id == determine_expected_commit_id(deployed_commit_id)
