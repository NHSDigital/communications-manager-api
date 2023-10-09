Scenario: An API consumer submitting a request when the backend service responds with a 504 timeout receives a 504 'Timeout' response
=====================================================================================================================================

| **Given** the backend service is too slow to be reached
| **When** the request is submitted
| **Then** the response is a 504 timeout error

**Asserts**
- Response returns a 504 'Timeout' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst