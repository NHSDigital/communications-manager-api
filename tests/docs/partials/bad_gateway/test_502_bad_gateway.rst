Scenario: An API consumer submitting a request when the backend service responds with a 502 Bad Gateway error
=====================================================================================================================================

| **Given** the backend service is unable to call a downstream service
| **When** the request is submitted
| **Then** the response is a 502 bad gateway error

**Asserts**
- Response returns a 502 'Bad Gateway' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst