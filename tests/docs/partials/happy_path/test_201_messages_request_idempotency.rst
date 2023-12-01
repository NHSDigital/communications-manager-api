Scenario: An API consumer submitting a message request with a messageReference used in a previous request recieves the same response as the original request
============================================================================================================================================================

| **Given** the API consumer submits a message request
| **And** the API consumer submits a second messages request containing the same messageReference as the first request
| **When** the request is submitted
| **Then** the response is the same contents as the first request

**Asserts**
- Response returns a 201 status code
- Response body matches the first request