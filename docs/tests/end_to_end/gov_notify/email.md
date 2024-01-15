# Email Tests

These tests check that the system can proccess a request to a users email end to end


## Scenario: An API consumer sending a request to target a user’s email can confirm the message is delivered

**Given** the API consumer submits a request targeting a user’s email
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>
**And** Gov Notify shows the message as delivered
<br/>

**Asserts**
- Response returns a 201 status code
- Message is present in Gov Notify as delivered
