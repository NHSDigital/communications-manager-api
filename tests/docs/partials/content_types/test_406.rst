Scenario: An API consumer submitting a request with an invalid accept header receives a 406 'Not Acceptable' response
=====================================================================================================================

| **Given** the API consumer provides an invalid accept header
| **When** the request is submitted
| **Then** the response is a 406 not acceptable error

**Asserts**
- API Recognises headers in case insensitive formats
- Response returns a 406 'Not Acceptable' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided
- Response returns the default content type if none is provided

.. include:: /partials/invalid_accept_headers.rst
.. include:: /partials/methods.rst
.. include:: /partials/correlation_ids.rst