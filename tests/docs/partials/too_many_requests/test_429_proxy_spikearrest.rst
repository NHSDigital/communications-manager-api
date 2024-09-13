Scenario: An API consumer submitting requests when exceeding the proxy spike arrest rate limit
=====================================================================================================================================

| **Given** A proxy spike arrest rate limit
| **When** requests exceeding that limit are submitted
| **Then** the response is a 429 Too Many Requests error

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body