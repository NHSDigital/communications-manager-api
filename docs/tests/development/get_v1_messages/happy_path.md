# Happy Path Tests

These tests target the API endpoint GET /v1/messages testing successful responses when valid data is provided.


## Scenario: An API consumer getting a message receives a 200 response

**Given** the API consumer provides a valid message ID when requesting a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer getting a message receives a 200 response for a message with multiple channel types

**Given** the API consumer provides a message ID for a message with multiple channel types when requesting a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>
**And** the expected response body is returned
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer getting a message receives a 200 response for a message with a status of ‘failed’

**Given** the API consumer provides a message ID for a message with a status in ‘failed’ when requesting a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>
**And** the expected response body is returned
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer getting a message receives a 200 response for a message with a status of ‘pending enrichment’

**Given** the API consumer provides a message ID for a message with a status in ‘pending enrichment’ when requesting a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>
**And** the expected response body is returned
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer getting a message receives a 200 response for a message with a status of ‘sending’

**Given** the API consumer provides a message ID for a message with a status in ‘sending’ when requesting a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>
**And** the expected response body is returned
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer getting a message receives a 200 response for a delivered message

**Given** the API consumer provides a message ID for a delivered message when requesting a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>
**And** the expected response body is returned
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI
