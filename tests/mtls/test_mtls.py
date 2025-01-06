"""
This test suite ensures that our mutual TLS security is enabled on
all of the environments.

This is important as it ensures that we have not accidentally disabled
mutual TLS post deployment, or by accidentally making a manual change
which causes it to become disabled.

These tests are run post deployment for:

* internal-dev
* uat
* int
* prod

They are also run every 10 minutes, with failures sent to Teams.
"""

import requests
import pytest
from lib.constants.constants import *


@pytest.mark.mtlstest
@pytest.mark.inttest
def test_mtls_connection_reset_by_peer_int():
    """
    Ensures that mTLS is enabled on the integration API backend service.
    """
    with pytest.raises(Exception) as e:
        requests.get(INT_API_GATEWAY_URL, headers={"X-Client-Id": "hello"})
    assert e.value is not None


@pytest.mark.mtlstest
@pytest.mark.devtest
def test_mtls_connection_reset_by_peer_dev():
    """
    Ensures that mTLS is enabled on the internal-dev API backend service.
    """
    with pytest.raises(Exception) as e:
        requests.get(DEV_API_GATEWAY_URL, headers={"X-Client-Id": "hello"})
    assert e.value is not None


@pytest.mark.mtlstest
@pytest.mark.prodtest
def test_mtls_connection_reset_by_peer_prod():
    """
    Ensures that mTLS is enabled on the production API backend service.
    """
    with pytest.raises(Exception) as e:
        requests.get(PROD_API_GATEWAY_URL, headers={"X-Client-Id": "hello"})
    assert e.value is not None


@pytest.mark.mtlstest
@pytest.mark.uattest
def test_mtls_connection_reset_by_peer_uat():
    """
    Ensures that mTLS is enabled on the UAT, API backend service.
    """
    with pytest.raises(Exception) as e:
        requests.get(UAT_API_GATEWAY_URL, headers={"X-Client-Id": "hello"})
    assert e.value is not None
