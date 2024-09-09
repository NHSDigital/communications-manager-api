Scenario: An API consumer submitting requests when exceeding the specific app spike arrest rate limit for another app
=====================================================================================================================================

| **Given** A specific app spike arrest rate limit is set for a different app
| **When** requests exceeding that limit are submitted
| **Then** the response is 200 OK

**Asserts**
- Response returns a 200 OK
- Response returns the expected message body