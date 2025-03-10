Scenario: An API consumer creating a message with an undefined NHS number receives a 201 response
==================================================================================================

| **Given** the API consumer does not provide an NHS number for the recipient in their new message and the allowAnonymousPatient flag is set to true
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI
