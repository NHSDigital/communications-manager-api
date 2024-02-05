Scenario: An API consumer sending a request to target a user's email can confirm the message is delivered
=========================================================================================================

| **Given** the API consumer submits a request targeting a user's email
| **When** the request is submitted
| **Then** the response is a 201 success
| **And** Gov Notify shows the message as delivered

**Asserts**
- Response returns a 201 status code
- Message is present in Gov Notify as delivered
