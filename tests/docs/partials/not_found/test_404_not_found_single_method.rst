Scenario: An API consumer submitting a request to an unknown endpoint receives a 404 'Not Found' response
=========================================================================================================

| **Given** the API consumer does not know how to identify the resource they want to fetch
| **When** the request is submitted to an unknown resource
| **Then** the service responds with a 404 not found response, telling the user the resource does not exist

**Asserts**
- Response returns a 404 'Not Found' error
- Response returns the expected error message body