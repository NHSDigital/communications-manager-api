Scenario: An API consumer submitting a request with an invalid authentication type receoves a 403 'Forbidden' response

| **Given** the API consumer provides an unaccepted authentication type
| **When** the request is submitted
| **Then** the response is a 403 forbidden error

**Asserts**
- Response returns a 403 'Forbidden' error
- Response returns the expected error message body

.. include:: /partials/methods.rst