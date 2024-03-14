Scenario: An API consumer sending a request to generate an nhs app message can confirm the message is delivered in the Internal Dev environment
===============================================================================================================================================

| **Given** the API consumer submits a request to generate an NHS App message
| **When** the request is submitted
| **Then** the response is a 201 success
| **And** The GET message endpoint shows the message as delivered

**Asserts**
- Response returns a 201 status code
- Message is reported as delivered by the GET message endpoint
