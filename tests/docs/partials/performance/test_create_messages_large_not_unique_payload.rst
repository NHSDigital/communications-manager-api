Scenario: An API consumer submitting a request with a large request body containing 50,000 duplicate messages receives a 400 response
=====================================================================================================================================

| **Given** the API consumer provides a message body of 50,000 duplicate messages
| **When** the request is submitted
| **Then** the response is a 400 invalid value error
| **And** the response body contains 100 errors
| **And** the response takes less than 29 seconds

**Asserts**
- Response returns a 400 'Invalid Value' status code
- Response returns 100 error message blocks