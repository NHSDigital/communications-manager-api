# Happy Path Tests

These tests target the API endpoint GET /v1/messages/{messageId} testing successful responses when valid data is provided.


## Scenario: An API consumer getting a message receives a 200 response

**Given** the API consumer provides a valid message ID when requesting a message
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted link to new message URI


<!-- include: ../../partials/happy_path/test_200_get_message_valid_response_bodies.rst -->
