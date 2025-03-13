Scenario: An API consumer submitting a request with cors headers receives a response reflecting the cors headers values
=======================================================================================================================

.. include:: /partials/cors.rst

| **Given** the API consumer wants to make a request using CORS
| **When** a browser is used to send the initial OPTIONS request
| **Then** the response allows the request proper to be sent

**Asserts**
- Response returns 200 status code
- Response contains 'Access-Control-Allow-Origin' header matching the provided value
- Response contains 'Access-Control-Allow-Methods' header matching the provided HTTP method supplied
- Response contains 'Access-Control-Max-Age' headers matching the maximum age allow methods and headers can be cached (42 days)
- Response contains 'Access-Control-Allow-Headers' headers matching the API's allowed headers
- Response contains 'Cross-Origin-Resource-Policy' header matching 'cross-origin'