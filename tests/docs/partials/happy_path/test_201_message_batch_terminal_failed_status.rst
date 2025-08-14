Scenario: An API consumer creating a message that has a terminal status of FAILED
=================================================================================

| **Given** the API consumer provides details for an unreachable recipient in their new message
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI
- Message in NHS Notify reaches terminal status of FAILED
- Message has expected failure reason and code
- Channel has expected failure reason and code
