Scenario: An API consumer submitting a GET NHS App Accounts request without an ODS Code
=========================================================================================================

| **Given** the API consumer sends a request to get NHS App Accounts without providing an ODS Code
| **When** the request is submitted
| **Then** the service responds with a 400 invalid response, telling the user the ODS Code is missing

**Asserts**
- Response returns a 400 'Invalid' error
- Response returns the expected error message body

.. include:: /partials/nhsapp_accounts_pages.rst