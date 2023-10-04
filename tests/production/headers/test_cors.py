import requests
import pytest
from lib import Assertions, Authentication
from lib.constants import *


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.prodtest
@pytest.mark.parametrize("method", METHODS)
def test_cors_options(method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with cors \
        headers receives a response reflecting the cors headers values

        .. include:: ../../partials/cors.rst

        | **Given** the API consumer wants to make a request using CORS
        | **When** a browser is used to send the initial OPTIONS request
        | **Then** the response allows the request proper to be sent

    **Asserts**
    - Response returns 200 status code
    - Response contains 'Access-Control-Allow-Origin' header matching the provided value
    - Response contains 'Access-Control-Allow-Methods' header matching the provided HTTP method supplied
    - Response contains 'Access-Control-Max-Age' headers matching the maximum age allow methods and headers \
        can be cached (42 days)
    - Response contains 'Access-Control-Allow-Headers' headers matching the API's allowed headers
    - Response contains 'Cross-Origin-Resource-Policy' header matching 'cross-origin'
    """
    resp = requests.options(f"{PROD_URL}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, "https://my.website")


@pytest.mark.prodtest
@pytest.mark.parametrize("method", TEST_METHODS)
def test_cors(method):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an 'Origin' header receives \
    the expected cors headers in response

        .. include:: ../../partials/cors.rst

        | **Given** the API consumer provides an Origin header
        | **When** the request is submitted
        | **Then** the response contains CORS headers to allow the request

    **Asserts**
    - Response contains 'Access-Control-Allow-Origin' header matching the provided value
    - Response contains 'Access-Control-Expose-Headers' header matching 'x-correlation-id'
    - Response contains 'Cross-Origin-Resource-Policy' header matching 'cross-origin'

    .. include:: ../../partials/methods.rst
    """
    resp = getattr(requests, method)(f"{PROD_URL}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")
