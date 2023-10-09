Scenario: An API consumer creating a batch of messages with a valid accept header receives a 201 response
=========================================================================================================

| **Given** the API consumer provides a valid accept header when creating a batch of messages
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code