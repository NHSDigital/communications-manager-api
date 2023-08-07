import requests
import pytest
from lib.constants import *


@pytest.mark.mtlstest
@pytest.mark.inttest
def test_mtls_connection_reset_by_peer_int():
    with pytest.raises(Exception) as e:
        requests.get(INT_API_GATEWAY_URL, headers={"X-Client-Id": "hello"})
    assert("Connection reset by peer" in str(e.value))


@pytest.mark.mtlstest
@pytest.mark.devtest
def test_mtls_connection_reset_by_peer_dev():
    with pytest.raises(Exception) as e:
        requests.get(DEV_API_GATEWAY_URL, headers={"X-Client-Id": "hello"})
    assert("Connection reset by peer" in str(e.value))


@pytest.mark.mtlstest
@pytest.mark.prodtest
def test_mtls_connection_reset_by_peer_prod():
    with pytest.raises(Exception) as e:
        requests.get(PROD_API_GATEWAY_URL, headers={"X-Client-Id": "hello"})
    assert("Connection reset by peer" in str(e.value))
