Scenario: An API consumer wants to test the service ban error message on the sandbox environment
================================================================================================

| **Given** the API consumer provides a code 403.1 prefer header
| **When** the request is submitted
| **Then** the response returns a 403 service ban error

**Asserts**
- Response returns a 403 'Service Ban' error
- Response returns the expected error message body referencing the Authorization header
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst