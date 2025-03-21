# Happy Path Tests

These tests target the API endpoint POST /v1/messages testing successful responses when valid data is provided.


## Scenario: An API consumer creating a message with an undefined NHS number receives a 201 response

**Given** the API consumer does not provide an NHS number for the recipient in their new message and the allowAnonymousPatient flag is set to true
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>

**Asserts**
- Response returns a 201 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


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


## Scenario: An API consumer creating a message with valid contact details receives a 201 response

**Given** the API consumer provides valid contact details for the recipient in their new message
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
