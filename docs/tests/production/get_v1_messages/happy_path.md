# Happy Path Tests

These tests target the API endpoint GET /v1/messages testing successful responses when valid message ids are provided.


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

**Valid message IDs**

This test uses message id values to retrieve successful responses from the API.

Below is a list of the message ids used on the integration and production environments that retrieve a message status for a batch and single message.

| Message Retreived   | Message ID                  |
|---------------------|-----------------------------|
| Message Batch       | 2aUxdGDkW87biAvPOfG8ATYHj00 |
| Single Message      | 2aUxQER3co3kXdvTKrhbSFHRRxR |
