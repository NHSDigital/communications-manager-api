Scenario: An API consumer submitting a request with a routing plan referencing the same template twice receives a 500 'Duplicate Routing Plan' response
=======================================================================================================================================================

| **Given** the API consumer provides a message body containing a reference to the same template twice
| **When** the request is submitted
| **Then** the response returns a 500 duplicate routing plan error

**Asserts**
- Response returns a 500 'Duplicate Routing Plan' error
- Response returns the expected error message body referencing the duplicate template values