Scenario: An API consumer sending a request to generate a letter can confirm the message is received in Gov Notify in the Internal Dev environment
==================================================================================================================================================

| **Given** the API consumer submits a request to generate a letter
| **When** the request is submitted
| **Then** the response is a 201 success
| **And** Gov Notify shows the message as received

**Asserts**
- Response returns a 201 status code
- Message is present in Gov Notify as received
