Scenario: An API consumer submitting a request with an invalid date of birth receives a 400 'Invalid Value' response
====================================================================================================================

A valid date of birth must be structured in this format: YYYY-MM-dd

| **Given** the API consumer provides an message body with an invalid date of birth
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst