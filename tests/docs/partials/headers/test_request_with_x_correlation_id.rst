Scenario: An API consumer submitting a request with to a request with an 'X-Correlation-Id' header receives a response reflecting the X-Correlation-Id value
============================================================================================================================================================

| **Given** the API consumer provides an x-correlation-id header
| **When** the request is submitted
| **Then** the response is contains an x-correlation-id header

**Asserts**
- Response returns a 504 status code
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: /partials/methods.rst
.. include:: /partials/correlation_ids.rst