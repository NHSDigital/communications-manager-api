Scenario: An API comsumer submitting a request with a 403 prefer header receives a 403 'Forbidden' response
===========================================================================================================

| **Given** the API consumer provides a 401 prefer header
| **When** the request is submitted
| **Then** the response is a 401 access denied error

**Asserts**
- Response returns a 401 'Access Denied' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/methods.rst
.. include:: ../../partials/correlation_ids.rst