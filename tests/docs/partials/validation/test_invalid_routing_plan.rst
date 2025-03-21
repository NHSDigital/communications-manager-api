Scenario: An API consumer submitting a request with an invalid routing plan receives a 400 'Invalid Value' response
===================================================================================================================

The routing plan must be in a UUID format, for more information on UUID, look `here <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__

| **Given** the API consumer provides an message body with an invalid routing plan
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body with references to the invalid attribute