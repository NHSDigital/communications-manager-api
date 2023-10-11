Scenario: An API consumer submitting a request with a 408 prefer header receives a 408 'Timeout' response
=========================================================================================================

| **Given** the API consumer provides a 408 prefer header
| **When** the request is submitted
| **Then** the response is a 408 timeout error

**Asserts**
- Response returns a 408 'Timeout' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst