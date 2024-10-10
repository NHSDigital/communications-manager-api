# Happy Path Tests

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


### Scenario: An API consumer submitting a message batches request with a messageBatchReference used in a previous request recieves the same response as the original request

**Given** the API consumer submits a message batches request
<br/>
**And** the API consumer submits a second message batches request containing the same messageBatchReference as the first request
<br/>
**When** the request is submitted
<br/>
**Then** the response is the same contents as the first request
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches the first request


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
