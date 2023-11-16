Scenario: An API consumer getting a message receives a 200 response
===============================================================================================================

| **Given** the API consumer provides a valid message ID when requesting a message
| **When** the request is submitted
| **Then** the response is a 200 success

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI