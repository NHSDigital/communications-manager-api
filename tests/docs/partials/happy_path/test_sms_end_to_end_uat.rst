Scenario: An API consumer sending a request to generate an SMS can confirm the message is delivered in Gov Notify in the UAT environment
========================================================================================================================================

| **Given** the API consumer submits a request to generate an SMS
| **When** the request is submitted
| **Then** the response is a 201 success
| **And** Gov Notify shows the message as delivered

**Asserts**
- Response returns a 201 status code
- Message is present in Gov Notify as delivered
