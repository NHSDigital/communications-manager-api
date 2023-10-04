import requests
import pytest
from lib import Assertions


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]
ORIGIN = "https://my.website"


@pytest.mark.devtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_options(nhsd_apim_proxy_url, method, nhsd_apim_auth_headers):
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
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": ORIGIN,
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, ORIGIN)


@pytest.mark.devtest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors(nhsd_apim_proxy_url, method, nhsd_apim_auth_headers):
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
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": ORIGIN
    })

    Assertions.assert_cors_headers(resp, ORIGIN)
