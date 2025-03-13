Scenario: An API consumer has sent a duplicate request
======================================================================================================================

| **Given** an API consumer
| **When** a duplicate request is submitted
| **Then** the response returns a 422 duplicate request error

**Asserts**
- Response returns a 422 'Duplicate Request' error