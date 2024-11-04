Scenario: An API consumer creating a batch of messages with a valid routing plan header receives a 201 response
===============================================================================================================

| **Given** the API consumer provides a valid routing plan when creating a batch of messages
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI