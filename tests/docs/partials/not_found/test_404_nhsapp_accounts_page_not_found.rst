Scenario: An API consumer submitting a GET NHS App Accounts request with a page that does not exist
=========================================================================================================

| **Given** the API consumer sends a request to get NHS App Accounts with a valid ODS code and a page that does not exist
| **When** the request is submitted
| **Then** the service responds with a 404 not found response, telling the user the resource does not exist

**Asserts**
- Response returns a 404 'Not Found' error
- Response returns the expected error message body