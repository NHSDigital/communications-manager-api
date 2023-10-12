# Header Tests

# /v1/message-batches

## CORS Responses


### Scenario: An API consumer submitting a request with an ‘Origin’ header receives the expected cors headers in response

CORS allows the API to be used whilst within a web browser, from websites that are hosted on a different domain to that of the API. This is important as users utilising our API documentation must be able to send test requests from that page using the ‘try it now’ functionality.

**Given** the API consumer provides an Origin header
<br/>
**When** the request is submitted
<br/>
**Then** the response contains CORS headers to allow the request
<br/>

**Asserts**
- Response contains ‘Access-Control-Allow-Origin’ header matching the provided value
- Response contains ‘Access-Control-Expose-Headers’ header matching ‘x-correlation-id’
- Response contains ‘Cross-Origin-Resource-Policy’ header matching ‘cross-origin’

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


### Scenario: An API consumer submitting a request with cors headers receives a response reflecting the cors headers values

CORS allows the API to be used whilst within a web browser, from websites that are hosted on a different domain to that of the API. This is important as users utilising our API documentation must be able to send test requests from that page using the ‘try it now’ functionality.

**Given** the API consumer wants to make a request using CORS
<br/>
**When** a browser is used to send the initial OPTIONS request
<br/>
**Then** the response allows the request proper to be sent
<br/>

**Asserts**
- Response returns 200 status code
- Response contains ‘Access-Control-Allow-Origin’ header matching the provided value
- Response contains ‘Access-Control-Allow-Methods’ header matching the provided HTTP method supplied
- Response contains ‘Access-Control-Max-Age’ headers matching the maximum age allow methods and headers can be cached (42 days)
- Response contains ‘Access-Control-Allow-Headers’ headers matching the API’s allowed headers
- Response contains ‘Cross-Origin-Resource-Policy’ header matching ‘cross-origin’

## Correlation Id


### Scenario: An API consumer submitting a request with to a request with an ‘X-Correlation-Id’ header receives a response reflecting the X-Correlation-Id value

**Given** the API consumer provides an x-correlation-id header
<br/>
**When** the request is submitted
<br/>
**Then** the response is contains an x-correlation-id header
<br/>

**Asserts**
- Response returns a 504 status code
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

# /v1/messages

## CORS Responses


### Scenario: An API consumer submitting a request with an ‘Origin’ header receives the expected cors headers in response

CORS allows the API to be used whilst within a web browser, from websites that are hosted on a different domain to that of the API. This is important as users utilising our API documentation must be able to send test requests from that page using the ‘try it now’ functionality.

**Given** the API consumer provides an Origin header
<br/>
**When** the request is submitted
<br/>
**Then** the response contains CORS headers to allow the request
<br/>

**Asserts**
- Response contains ‘Access-Control-Allow-Origin’ header matching the provided value
- Response contains ‘Access-Control-Expose-Headers’ header matching ‘x-correlation-id’
- Response contains ‘Cross-Origin-Resource-Policy’ header matching ‘cross-origin’

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


### Scenario: An API consumer submitting a request with cors headers receives a response reflecting the cors headers values

CORS allows the API to be used whilst within a web browser, from websites that are hosted on a different domain to that of the API. This is important as users utilising our API documentation must be able to send test requests from that page using the ‘try it now’ functionality.

**Given** the API consumer wants to make a request using CORS
<br/>
**When** a browser is used to send the initial OPTIONS request
<br/>
**Then** the response allows the request proper to be sent
<br/>

**Asserts**
- Response returns 200 status code
- Response contains ‘Access-Control-Allow-Origin’ header matching the provided value
- Response contains ‘Access-Control-Allow-Methods’ header matching the provided HTTP method supplied
- Response contains ‘Access-Control-Max-Age’ headers matching the maximum age allow methods and headers can be cached (42 days)
- Response contains ‘Access-Control-Allow-Headers’ headers matching the API’s allowed headers
- Response contains ‘Cross-Origin-Resource-Policy’ header matching ‘cross-origin’

## Correlation Id


### Scenario: An API consumer submitting a request with to a request with an ‘X-Correlation-Id’ header receives a response reflecting the X-Correlation-Id value

**Given** the API consumer provides an x-correlation-id header
<br/>
**When** the request is submitted
<br/>
**Then** the response is contains an x-correlation-id header
<br/>

**Asserts**
- Response returns a 504 status code
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
