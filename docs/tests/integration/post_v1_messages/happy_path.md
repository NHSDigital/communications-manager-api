# Happy Path Tests

These tests target the API endpoint POST /v1/messages testing successful responses when valid data is provided.


## Scenario: An API consumer creating a message with a valid accept header receives a 201 response

**Given** the API consumer provides a valid accept header when creating a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer creating a message with a valid content type header receives a 201 response

**Given** the API consumer provides a valid content type header when creating a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer creating a message with a valid date of birth receives a 201 response

**Given** the API consumer provides a valid date of birth for the recipient in their new message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer creating a message with a valid NHS number receives a 201 response

**Given** the API consumer provides a valid NHS number for the recipient in their new message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer creating a message with a valid routing plan header receives a 201 response

**Given** the API consumer provides a valid routing plan when creating in their new message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


## Scenario: An API consumer submitting a message request with a messageReference used in a previous request recieves the same response as the original request

**Given** the API consumer submits a message request
<br/>
**And** the API consumer submits a second messages request containing the same messageReference as the first request
<br/>
**When** the request is submitted
<br/>
**Then** the response is the same contents as the first request
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches the first request


## Scenario: An API consumer creating a message with a date of birth receives a 201 response

**Given** the API consumer does not provide a date of birth for the recipient in their new message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI
