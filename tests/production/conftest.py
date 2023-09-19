import pytest
import requests
import time


@pytest.fixture(autouse=True)
def send_request():
    yield requests
    time.sleep(1)
