Scenario: An API consumer creating a message with a valid date of birth receives a 201 response
=========================================================================================================

| **Given** the API consumer provides a valid date of birth for the recipient in their new message
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI
