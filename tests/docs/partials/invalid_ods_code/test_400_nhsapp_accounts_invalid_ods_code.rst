Scenario: An API consumer submitting a GET NHS App Accounts request an invalid ODS Code
=========================================================================================================

| **Given** the API consumer sends a request to get NHS App Accounts with an invalid ODS Code
| **When** the request is submitted
| **Then** the service responds with a 400 invalid response, telling the user the ODS Code is invalid

**Asserts**
- Response returns a 400 'Invalid' error
- Response returns the expected error message body
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst
.. include:: ../../partials/nhsapp_accounts_pages.rst