Scenario: An API consumer submitting a request to an endpoint with an invalid method receives a 405 'Not Allowed' response
==========================================================================================================================

| **Given** the API consumer does not know an allowed method on a resource they want to interact with
| **When** the request is submitted with a method is not allowed
| **Then** the service responds with a 405 not allowed response, telling the user the method is not allowed

**Asserts**
- Response returns a 405 'Not Allowed' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/methods.rst
.. include:: ../../partials/correlation_ids.rst
