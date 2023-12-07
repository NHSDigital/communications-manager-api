Scenario: An API consumer creating a message with a valid content type header receives a 201 response
===============================================================================================================

| **Given** the API consumer provides a valid content type header when creating a message
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI
