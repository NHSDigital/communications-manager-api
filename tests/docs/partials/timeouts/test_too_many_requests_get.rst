Scenario: An API consumer submitting a request with a 429 Prefer header receives a 429 'Quota' response
=======================================================================================================

| **Given** the API consumer provides a 429 prefer header
| **When** the request is submitted
| **Then** the response is a 429 quota error

**Asserts**
- Response returns a 429 'Quota' error
- Response returns 'Retry-After' header
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/methods.rst
.. include:: ../../partials/correlation_ids.rst
