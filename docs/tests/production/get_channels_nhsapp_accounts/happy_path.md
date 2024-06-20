# Happy Path Tests

These tests target the API endpoint GET /channels/nhsapp/accounts testing successful responses when valid data is provided.


## Scenario: An API consumer getting NHS App Accounts receives a 200 response

**Given** the API consumer provides a valid ODS Code for multiple paged results when requesting NHS App Accounts
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted links for self, next and last


## Scenario: An API consumer getting NHS App Accounts receives a 200 response

**Given** the API consumer provides a valid ODS Code for single paged results when requesting NHS App Accounts
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 200 success
<br/>

**Asserts**
- Response returns a 200 status code
- Response body matches expected result
- Response contains correctly formatted links for self and last
