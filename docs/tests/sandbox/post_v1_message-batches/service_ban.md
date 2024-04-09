# Service Ban


## Scenario: An API consumer has been banned from the service, when making requests they fail with a service ban response

**Given** the API consumer has been banned
<br/>
**When** a request is submitted
<br/>
**Then** the response returns a 403 service ban error
<br/>

**Asserts**
- Response returns a 403 ‘Service Ban’ error
- Response returns the expected error message body referencing the Authorization header
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


## Scenario: An API consumer wants to test the service ban error message on the sandbox environment

**Given** the API consumer provides a code 403.1 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 403 service ban error
<br/>

**Asserts**
- Response returns a 403 ‘Service Ban’ error
- Response returns the expected error message body referencing the Authorization header
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |
