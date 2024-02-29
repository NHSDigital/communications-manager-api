# NHS App Tests

These tests check that the system can proccess a request to a users nhs app account end to end


## Scenario: An API consumer sending a request to generate an nhs app message can confirm the message is delivered

**Given** the API consumer submits a request to generate an NHS App message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>
**And** The GET message endpoint shows the message as delivered
<br/>

**Asserts**
- Response returns a 201 status code
- Message is reported as delivered by the GET message endpoint
