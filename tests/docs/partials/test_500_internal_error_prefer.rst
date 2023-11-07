Scenario: An API consumer submitting a request with a 500 prefer header receives a 500 'internal server error' response
=======================================================================================================================

| **Given** the API consumer provides a 500 prefer header
| **When** the request is submitted
| **Then** the response is a 500 internal server error

**Asserts**
- Response returns a 500 'internal server' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst
