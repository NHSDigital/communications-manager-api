Scenario: An API consumer submitting a request with a request body containing 45,000 messages between 6MB and 10MB receives a 413 status code and response body containing an instance of that error
====================================================================================================================================================================================================

| **Given** the API consumer provides a message body of 45,000 messages between 6MB and 10MB
| **When** the request is submitted
| **Then** the response is a 413 Request Entity Too Large
| **And** the response body contains 1 error

**Asserts**
- Response returns a 413 'Request Entity Too Large' status code
- Response returns 1 error message block
