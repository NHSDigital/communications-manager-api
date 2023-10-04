Scenario: An API consumer submitting a request with a code 504 Prefer header receives a 504 'Timeout' error response
====================================================================================================================

| **Given** the API consumer provides a code 504 prefer header
| **When** the request is submitted
| **Then** the response is a 504 timeout error

**Asserts**
- Response returns a 504 'Timeout' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst