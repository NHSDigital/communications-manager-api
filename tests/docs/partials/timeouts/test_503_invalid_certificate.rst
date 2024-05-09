Scenario: An API consumer submitting a request to simulate an invalid certificate error from the back end
=====================================================================================================================

| **Given** the API consumer uses the path _invalid_certificate
| **When** the request is submitted
| **Then** the response is a 503 service unavailable error

**Asserts**
- Response returns a 503 'Service Unavailable' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst