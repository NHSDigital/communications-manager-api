import requests
import pytest
from lib import Assertions, Generators
from lib.constants import *


MOCK_TOKEN = {
    "Authorization": "Bearer InvalidMockToken"
}


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid(nhsd_apim_proxy_url, correlation_id, method):
    """
    .. py:function:: Test 401 responses

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc fermentum finibus eros id pulvinar. Aliquam erat volutpat. Praesent iaculis congue pretium. Nullam consequat at velit ut iaculis. Suspendisse pulvinar tempor ex, id facilisis justo varius sed. Proin pulvinar odio ut dui pulvinar, sed semper neque porttitor. Sed vel faucibus mi. Donec sit amet velit mollis, venenatis erat nec, facilisis tortor. Cras ac eros hendrerit sapien gravida mattis. Duis posuere posuere urna. Nunc vel ornare erat. Cras rhoncus lacus metus, ut facilisis ligula tempor at. Donec ultricies elit ut arcu lacinia consectetur. Integer non lacus luctus, finibus enim eget, mollis erat.

    Morbi ut condimentum diam, tempus interdum arcu. Pellentesque est quam, elementum ac aliquet vitae, eleifend sed diam. Donec eleifend gravida justo, sed finibus orci ornare quis. Integer suscipit lacus at suscipit commodo. Mauris vel sodales eros. Cras viverra rutrum sodales. Nullam nec sapien pharetra, viverra lorem sit amet, rutrum nulla. Phasellus sit amet erat eu massa condimentum pellentesque.

    Vestibulum tempus velit vitae tellus suscipit, euismod consectetur est mattis. Etiam eget cursus dui. Donec dignissim quis neque sed imperdiet. Etiam a consectetur risus. Donec a est enim. Curabitur ac odio non diam faucibus maximus. Nulla ut magna pulvinar, laoreet nunc non, finibus lectus. Etiam efficitur eleifend lectus, semper interdum magna molestie nec.

    Nullam pellentesque ornare leo id rhoncus. Suspendisse varius auctor ex, quis feugiat urna fermentum ut. Nullam tincidunt neque sit amet mi tincidunt tristique. Nulla dignissim massa eget felis bibendum, sed efficitur arcu gravida. Donec semper arcu sed lorem maximus feugiat. In consequat consequat sapien sed consectetur. Vestibulum efficitur, purus a egestas molestie, tortor elit ultricies diam, rutrum lacinia lectus neque eu diam. Fusce vestibulum auctor condimentum. Sed viverra laoreet quam a tempor. In vitae nulla et mauris viverra lacinia vel laoreet turpis. Praesent tortor odio, cursus a porttitor aliquam, molestie eu dui.

    Morbi at laoreet justo. Fusce aliquam tellus quam, sit amet aliquam tortor interdum sed. Suspendisse placerat leo et ultrices aliquam. Cras imperdiet, magna ut ullamcorper faucibus, est quam condimentum nunc, sed venenatis elit ipsum in erat. Mauris at velit id ex tempor fringilla vitae et lorem. Nulla facilisi. Maecenas sit amet odio in neque tempus feugiat. Vestibulum accumsan arcu orci, eget aliquet felis venenatis vitae.

    :param nhsd_apim_proxy_url: The URL of the proxy that the request will be sent to.
    :param correlation_id: The correlation id value to be sent in the `X-Correlation-Id` header.
    :param method: The HTTP method to test.

    :asserts: Asserts that the request fails with a 401 response code, validating that the error response body is correctly formed.

    .. include:: ../partials/correlation_ids.rst
    """
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        **MOCK_TOKEN,
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )

test_401_invalid.__name__ = "hello there"


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("method", METHODS)
def test_401_invalid_prefer(nhsd_apim_proxy_url, correlation_id, method):
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        "Prefer": "code=401",
        "X-Correlation-Id": correlation_id
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        401,
        Generators.generate_access_denied_error() if method not in ["options", "head"] else None,
        correlation_id
    )
