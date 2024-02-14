# Letter Tests

These tests check that the system can proccess a request to a users postal address end to end


## Scenario: An API consumer sending a request to generate a letter can confirm the message is received in Gov Notify

**Given** the API consumer submits a request to generate a letter
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 201 success
<br/>
**And** Gov Notify shows the message as received
<br/>

**Asserts**
- Response returns a 201 status code
- Message is present in Gov Notify as received
