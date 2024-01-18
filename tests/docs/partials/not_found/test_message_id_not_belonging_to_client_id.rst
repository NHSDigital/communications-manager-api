Scenario: An API consumer submitting a get message request with a message id belonging to another client receives a 404 'Not Found' response
============================================================================================================================================

| **Given** the API consumer submits a get message request with a message id belonging to another client
| **When** the request is submitted
| **Then** the service responds with a 404 not found response, telling the user the resource does not exist

**Asserts**
- Response returns a 404 'Not Found' error
- Response returns the expected error message body