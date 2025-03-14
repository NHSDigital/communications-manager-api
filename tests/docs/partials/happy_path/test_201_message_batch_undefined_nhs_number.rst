Scenario: An API consumer creating a batch of messages with an undefined NHS number receives a 201 response
===========================================================================================================

| **Given** the API consumer does not provide an NHS number for a recipient in their new message batch and the allowAnonymousPatient flag is set to true
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids