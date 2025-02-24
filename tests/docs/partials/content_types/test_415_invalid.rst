Scenario: An API consumer submitting a request with an invalid content type receives a 415 'Unsupported Media' response
=======================================================================================================================

| **Given** the API consumer provides an invalid content type header
| **When** the request is submitted
| **Then** the response is a 415 unsupported media error

**Asserts**
- API Recognises headers in case insensitive formats
- Response returns a 415 'Unsupported Media' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided
- Response returns the default content type if none is provided

.. include:: /partials/invalid_content_type_headers.rst
.. include:: /partials/methods.rst
.. include:: /partials/correlation_ids.rst