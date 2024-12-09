Scenario: An API consumer submitting a request with a missing accept header receives a 201 'Success' response
=============================================================================================================

| **Given** the API consumer does not provide an accept header
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids