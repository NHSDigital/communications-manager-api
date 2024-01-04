Scenario: An API consumer getting a message receives a 200 response for a message with multiple channel types
=============================================================================================================

| **Given** the API consumer provides a message ID for a message with multiple channel types when requesting a message
| **When** the request is submitted
| **Then** the response is a 200 success
| **And** the expected response body is returned

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI