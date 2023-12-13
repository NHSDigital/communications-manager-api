Scenario: An API consumer submitting a request when the backend service responds with a 408 timeout receives a 504 'Gateway Timeout' response
==============================================================================================================================================

| **Given** the backend service takes too long to respond
| **When** the request is submitted
| **Then** the response is a transformed from a 408 timeout error to a 504 gateway error

**Asserts**
- Response returns a 504 'Gateway Timeout' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst
