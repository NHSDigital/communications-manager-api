# Happy Path Tests

These tests target the API endpoint v1/message-batches testing successful responses when valid data is provided.

## 201 - Success


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


### Scenario: An API consumer creating a batch of messages with a valid date of birth receives a 201 response

**Given** the API consumer provides a valid date of birth for a recipient in their new message batch
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


### Scenario: An API consumer creating a batch of messages with a valid routing plan header receives a 201 response

**Given** the API consumer provides a valid routing plan when creating a batch of messages
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


### Scenario: An API consumer creating a batch of messages with a date of birth receives a 201 response

**Given** the API consumer does not provide a date of birth for a recipient in their new message batch
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
