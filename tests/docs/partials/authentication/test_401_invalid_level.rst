Scenario: An API consumer submitting a request with authentication with insufficient access receives a 401 'Access Denied' response
===================================================================================================================================

| **Given** the API consumer provides authentication with insufficient access
| **When** the request is submitted
| **Then** the response is a 401 access denied error


**Asserts**
- Response returns a 401 'Access Denied' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: /partials/methods.rst
