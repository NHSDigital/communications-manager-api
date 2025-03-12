# Happy Path Tests

## 201 - Success


### Scenario: An API consumer creating a batch of messages with an undefined NHS number receives a 201 response

**Given** the API consumer does not provide an NHS number for a recipient in their new message batch and the allowAnonymousPatient flag is set to true
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids


### Scenario: An API consumer creating a batch of messages with a valid accept header receives a 201 response

**Given** the API consumer provides a valid accept header when creating a batch of messages
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids


### Scenario: An API consumer creating a batch of messages with valid contact details receives a 201 response

**Given** the API consumer provides valid contact details for a recipient in their new message batch
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids


### Scenario: An API consumer creating a batch of messages with a valid content type header receives a 201 response

**Given** the API consumer provides a valid content type header when creating a batch of messages
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids


### Scenario: An API consumer creating a batch of messages with a valid NHS number receives a 201 response

**Given** the API consumer provides a valid NHS number for a recipient in their new message batch
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids
