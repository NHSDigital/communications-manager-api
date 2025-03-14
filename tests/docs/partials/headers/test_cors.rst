Scenario: An API consumer submitting a request with an 'Origin' header receives the expected cors headers in response
=====================================================================================================================

.. include:: ../../partials/cors.rst

| **Given** the API consumer provides an Origin header
| **When** the request is submitted
| **Then** the response contains CORS headers to allow the request

**Asserts**
- Response contains 'Access-Control-Allow-Origin' header matching the provided value
- Response contains 'Access-Control-Expose-Headers' header matching 'x-correlation-id'
- Response contains 'Cross-Origin-Resource-Policy' header matching 'cross-origin'

.. include:: /partials/methods.rst