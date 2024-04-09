# Quota Tests

## 429 - Quota


### Scenario: An API consumer submitting a request with a 429 Prefer header receives a 429 ‘Quota’ response

**Given** the API consumer provides a 429 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 429 quota error
<br/>

**Asserts**
- Response returns a 429 ‘Quota’ error
- Response returns ‘Retry-After’ header
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Methods**

This test makes use of different HTTP methods, if the method is either HEAD or OPTIONS the test will not assert against the body of the response as none is returned.

| Value   |
|---------|
| GET     |
| POST    |
| PUT     |
| PATCH   |
| DELETE  |
| HEAD    |
| OPTIONS |

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |
