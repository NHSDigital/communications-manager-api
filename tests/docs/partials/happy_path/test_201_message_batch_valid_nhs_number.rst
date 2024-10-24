Scenario: An API consumer creating a batch of messages with a valid NHS number receives a 201 response
======================================================================================================

| **Given** the API consumer provides a valid NHS number for a recipient in their new message batch
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI