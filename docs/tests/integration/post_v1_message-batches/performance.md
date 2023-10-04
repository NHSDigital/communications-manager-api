# Performance Tests


### Scenario: An API consumer submitting a request with a         request body containing 50,000 invalid messages receives a 400 status code         and response body containing the first 100 instances of errors

**Given** the API consumer provides a message body of 50,000 invalid messages
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 400 invalid value error
<br/>
**And** the response body contains 100 errors
<br/>
**And** the response takes less than 29 seconds
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ status code
- Response returns 100 error message blocks


### Scenario: An API consumer submitting a request with a         large request body containing 50,000 duplicate messages receives a 400 response

**Given** the API consumer provides a message body of 50,000 duplicate messages
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 400 invalid value error
<br/>
**And** the response body contains 100 errors
<br/>
**And** the response takes less than 29 seconds
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ status code
- Response returns 100 error message blocks
