Scenario: An API consumer submitting a request with an invalid routing plan receives a 400 'Invalid Value' response
===================================================================================================================

| **Given** the API consumer provides a message body with a routing plan referencing an invalid template
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body referencing the invalid attribute
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst