# Retry Too Early


### An API consumer retrying a request while the         original request is still being processed receives a 425 error

**Given** the API consumer retries a request
<br/>
**When** the original request is still being processed
<br/>
**Then** the response returns a 425 retry too early error
<br/>

**Asserts**
- Response returns a 425 ‘Retry Too Early’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### An API consumer wants to test the retry too         early error message on the sandbox environment

**Given** the API consumer provides a code 425 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 425 retry too early error
<br/>

**Asserts**
- Response returns a 425 ‘Retry Too Early’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |
