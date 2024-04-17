Scenario: An API consumer getting NHS App Accounts receives a 200 response
===============================================================================================================

| **Given** the API consumer provides a valid ODS Code for single paged results when requesting NHS App Accounts
| **When** the request is submitted
| **Then** the response is a 200 success

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted links for self and last
