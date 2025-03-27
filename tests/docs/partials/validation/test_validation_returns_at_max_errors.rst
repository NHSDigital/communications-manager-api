Scenario: An API consumer submitting a request with that will generate a set number of errors will receive a response containing references to each error up to 100 occurences
==============================================================================================================================================================================

| **Given** the API consumer provides an message body with that will generate a given number of errors
| **When** the request is submitted
| **Then** the response returns a 400 invalid value response
| **And** the response returns a message body referencing up to 100 errors

**Asserts**
- Response returns the expected number of errors