Scenario: An API consumer submitting a request when the backend service responds with a 429 Too Many Requests error
=====================================================================================================================================

| **Given** the backend service is unable to call a downstream service because the quota has been reached
| **When** the request is submitted
| **Then** the response is a 429 Too Many Requests error

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst