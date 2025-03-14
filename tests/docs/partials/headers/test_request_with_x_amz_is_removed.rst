Scenario: An API consumer submitting a request with x-amz headers does not have x-amz headers returned
======================================================================================================

| **Given** the API consumer provides an x-amz header
| **When** the request is submitted
| **Then** the response is does not contains an x-amz header

**Asserts**
- Response does not contain x-amz headers