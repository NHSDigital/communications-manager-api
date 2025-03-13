Scenario: An API consumer submitting a request with an unknown routing plan receives a 404 'No Such Routing Plan' response
==========================================================================================================================

| **Given** the API consumer provides a message body with an unknown routing plan
| **When** the request is submitted
| **Then** the response returns a 404 no such routing plan error

**Asserts**
- Response returns a 404 'No Such Routing Plan' error
- Response returns the expected error message body
