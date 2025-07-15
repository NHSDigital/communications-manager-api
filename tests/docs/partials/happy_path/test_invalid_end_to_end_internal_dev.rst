Scenario: An API consumer sending a request with an invalid message sees the request transition to a failed status in the Internal Dev environment
==================================================================================================================================================

| **Given** the API consumer submits a request with an invalid message
| **When** the request is submitted
| **Then** the response is a 201 success
| **And** the request transitions to a failed status

**Asserts**
- Response returns a 201 status code
- Message is present in NHS Notify as failed
