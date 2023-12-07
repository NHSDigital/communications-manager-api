Scenario: An API consumer submitting a message batches request with a messageBatchReference used in a previous request recieves the same response as the original request
=========================================================================================================================================================================

| **Given** the API consumer submits a message batches request
| **And** the API consumer submits a second message batches request containing the same messageBatchReference as the first request
| **When** the request is submitted
| **Then** the response is the same contents as the first request

**Asserts**
- Response returns a 201 status code
- Response body matches the first request