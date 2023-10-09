Scenario: An API consumer has been banned from the service, when making requests they fail with a service ban response
======================================================================================================================

| **Given** the API consumer has been banned
| **When** a request is submitted
| **Then** the response returns a 403 service ban error

**Asserts**
- Response returns a 403 'Service Ban' error
- Response returns the expected error message body referencing the Authorization header
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst