# Error Tests


## Scenario: An API consumer submitting a request with a 500 prefer header receives a 500 ‘internal server error’ response

**Given** the API consumer provides a 500 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 500 internal server error
<br/>

**Asserts**
- Response returns a 500 ‘internal server’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |
