Scenario: An API consumer submitting a request with an personalisation field too large receives a 400 'Invalid personalisation' response
========================================================================================================================================

Personalisation fields must not be too large for their given template

| **Given** the API consumer provides a message body with a personalisation field that is too large
| **When** the request is submitted
| **Then** the response returns a 400 Invalid personalisation error

**Asserts**
- Response returns a 400 'Invalid personalisation' error
- Response returns the expected error message body with references to the invalid attribute
