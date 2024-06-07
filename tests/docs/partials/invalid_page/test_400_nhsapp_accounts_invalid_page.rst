Scenario: An API consumer submitting a GET NHS App Accounts request an invalid page
=========================================================================================================

| **Given** the API consumer sends a request to get NHS App Accounts with an invalid page
| **When** the request is submitted
| **Then** the service responds with a 400 invalid response, telling the user the page is invalid

**Asserts**
- Response returns a 400 'Invalid' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst