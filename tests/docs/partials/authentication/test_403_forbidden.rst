Scenario: An API consumer submitting a request with a forbidden authorization token receives a 403 'Forbidden' response
=======================================================================================================================

| **Given** the API consumer provides an forbidden authorization token
| **When** the request is submitted
| **Then** the response is a 403 forbidden error

**Asserts**
- Response returns a 403 'Forbidden' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/methods.rst
.. include:: ../../partials/correlation_ids.rst