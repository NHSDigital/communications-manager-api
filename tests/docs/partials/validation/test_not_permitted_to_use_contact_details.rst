Scenario: An API consumer submitting a request with an contact details when not allowed receives a 400 'Cannot set contact details' response
======================================================================================================================


| **Given** the API consumer provides a message body with contact details
| **When** the request is submitted
| **Then** the response returns a 400 Cannot set contact details error

**Asserts**
- Response returns a 400 'Cannot set contact details' error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the 'X-Correlation-Id' header if provided



