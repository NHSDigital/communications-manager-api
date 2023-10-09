Scenario: An API consumer submitting a request without a request body receives a 400 'Invalid Value' response
=============================================================================================================

| **Given** the API consumer provides an empty message body
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst