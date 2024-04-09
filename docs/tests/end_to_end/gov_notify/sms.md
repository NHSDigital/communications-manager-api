# SMS Tests

These tests check that the system can proccess a request to a users SMS end to end


## Scenario: An API consumer sending a request to generate an SMS can confirm the message is delivered in Gov Notify in the Internal Dev environment

**Given** the API consumer submits a request to generate an SMS
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


## Scenario: An API consumer sending a request to generate an SMS can confirm the message is delivered in Gov Notify in the UAT environment

**Given** the API consumer submits a request to generate an SMS
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
