import requests
import pytest
from lib import Assertions, Generators

CORRELATION_IDS = [None, "b1ad9302-5df9-4066-bcd2-b274cfab1e72"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_408_timeout(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request \
        when the backend service responds with a 408 timeout \
            receives a 408 'Timeout' response

        | **Given** the backend service takes too long to respond
        | **When** the request is submitted
        | **Then** the response is a 408 timeout error

    **Asserts**
    - Response returns a 408 'Timeout' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout_408", headers={
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        408,
        Generators.generate_request_timeout_error(),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_408_timeout_prefer(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        408 prefer header receives a 408 'Timeout' response

        | **Given** the API consumer provides a 408 prefer header
        | **When** the request is submitted
        | **Then** the response is a 408 timeout error

    **Asserts**
    - Response returns a 408 'Timeout' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        "Prefer": "code=408",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        408,
        Generators.generate_request_timeout_error(),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_504_timeout(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request \
        when the backend service responds with a 504 timeout \
            receives a 504 'Timeout' response

        | **Given** the backend service is too slow to be reached
        | **When** the request is submitted
        | **Then** the response is a 504 timeout error

    **Asserts**
    - Response returns a 504 'Timeout' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst

    """
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout_504", headers={
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        504,
        Generators.generate_service_timeout_error(),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_504_timeout_simulate(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request \
        when the backend service responds with a 504 timeout after 3 seconds \
            receives a 504 'Timeout' response

        | **Given** the backend service is too slow to be reached
        | **When** the request is submitted
        | **Then** the response is a 504 timeout error

    **Asserts**
    - Response returns a 504 'Timeout' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}/_timeout?sleep=3000", headers={
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        504,
        Generators.generate_service_timeout_error(),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_504_timeout_prefer(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a \
        code 504 Prefer header receives a 504 'Timeout' error response

        | **Given** the API consumer provides a code 504 prefer header
        | **When** the request is submitted
        | **Then** the response is a 504 timeout error

    **Asserts**
    - Response returns a 504 'Timeout' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.get(f"{nhsd_apim_proxy_url}", headers={
        "Prefer": "code=504",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        504,
        Generators.generate_service_timeout_error(),
        correlation_id
    )
