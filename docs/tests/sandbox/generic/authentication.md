# Authentication Tests

## 401 - Access Denied


### Scenario: An API consumer submitting a request with an invalid authorization token receives a 401 ‘Access Denied’ response

**Given** the API consumer provides an invalid authorization token
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 401 access denied error
<br/>

**Asserts**
- Response returns a 401 ‘Access Denied’ error
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


..include:: ../../partials/authentication/test_401_invalid_prefer.rst

## 403 - Forbidden


### Scenario: An API consumer submitting a request with a forbidden authorization token receives a 403 ‘Forbidden’ response

**Given** the API consumer provides an forbidden authorization token
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 403 forbidden error
<br/>

**Asserts**
- Response returns a 403 ‘Forbidden’ error
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


### Scenario: An API comsumer submitting a request with a 403 prefer header receives a 403 ‘Forbidden’ response

**Given** the API consumer provides a 403 prefer header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 403 forbidden error
<br/>

**Asserts**
- Response returns a 403 ‘Forbidden’ error
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
