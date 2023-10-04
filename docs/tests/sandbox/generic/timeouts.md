# Timeout Tests

## Server timeouts


### Scenario: An API consumer submitting a request with a 503 prefer header receives a 503 ‘Service Unavailable’ response

**Given** the API consumer provides a 503 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 503 service unavailable error
<br/>

**Asserts**
- Response returns a 503 ‘Service Unavailable’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request when the backend service responds with a 504 timeout receives a 504 ‘Timeout’ response

**Given** the backend service is too slow to be reached
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 504 timeout error
<br/>

**Asserts**
- Response returns a 504 ‘Timeout’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with a code 504 Prefer header receives a 504 ‘Timeout’ error response

**Given** the API consumer provides a code 504 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 504 timeout error
<br/>

**Asserts**
- Response returns a 504 ‘Timeout’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request when the backend service responds with a 504 timeout after 3 seconds receives a 504 ‘Timeout’ response

**Given** the backend service is too slow to be reached
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 504 timeout error
<br/>

**Asserts**
- Response returns a 504 ‘Timeout’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |

## Client timeouts


### Scenario: An API consumer submitting a request when the backend service responds with a 408 timeout receives a 408 ‘Timeout’ response

**Given** the backend service takes too long to respond
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 408 timeout error
<br/>

**Asserts**
- Response returns a 408 ‘Timeout’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with a 408 prefer header receives a 408 ‘Timeout’ response

**Given** the API consumer provides a 408 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 408 timeout error
<br/>

**Asserts**
- Response returns a 408 ‘Timeout’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |
