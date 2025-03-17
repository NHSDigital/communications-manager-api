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


### Scenario: An API consumer submitting a request with authentication with insufficient access receives a 401 ‘Access Denied’ response

**Given** the API consumer provides authentication with insufficient access
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

## 403 - Forbidden


Scenario: An API consumer submitting a request with an invalid authentication type receoves a 403 ‘Forbidden’ response

**Given** the API consumer provides an unaccepted authentication type
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
