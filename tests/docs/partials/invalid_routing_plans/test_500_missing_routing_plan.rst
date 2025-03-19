Scenario: An API consumer submitting a request with a routing plan referencing a missing template receives a 500 'Missing Routing Plan' response
================================================================================================================================================

| **Given** the API consumer provides a message body with a routing plan referencing a missing template
| **When** the request is submitted
| **Then** the response returns a 500 missing routing plan template error

**Asserts**
- Response returns a 500 'Missing Routing Plan Template' error
- Response returns the expected error message body