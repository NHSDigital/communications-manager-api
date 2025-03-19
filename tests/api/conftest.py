import pytest
import requests
import time
import os


@pytest.fixture(autouse=True)
def send_request():
    if os.environ['API_ENVIRONMENT'] == "prod":
        yield requests
        time.sleep(1)
    else:
        yield requests
