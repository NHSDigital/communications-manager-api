# Content Types

## Not acceptable


### Scenario: An API consumer submitting a request with an invalid         accept header receives a 406 'Not Acceptable' response

**Given** the API consumer provides an invalid accept header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 406 not acceptable error
<br/>

**Asserts**
- Response returns a 406 ‘Not Acceptable’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Accept Headers**

This test uses accept header values. The api accepts header values insensitive of the case used, however, accept headers must be in an acceptable format to be accepted and generate a successful response.

| Request Header Name   | Request Header Value   |
|-----------------------|------------------------|
| accept                | “”                     |
| accept                | application/xml        |
| accept                | image/png              |
| accept                | text/plain             |
| accept                | audio/mpeg             |
| accept                | xyz/abc                |
| ACCEPT                | “”                     |
| ACCEPT                | application/xml        |
| ACCEPT                | image/png              |
| ACCEPT                | text/plain             |
| ACCEPT                | audio/mpeg             |
| ACCEPT                | xyz/abc                |
| Accept                | “”                     |
| Accept                | application/xml        |
| Accept                | image/png              |
| Accept                | text/plain             |
| Accept                | audio/mpeg             |
| Accept                | xyz/abc                |
| AcCePt                | “”                     |
| AcCePt                | application/xml        |
| AcCePt                | image/png              |
| AcCePt                | text/plain             |
| AcCePt                | audio/mpeg             |
| AcCePt                | xyz/abc                |

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


### Scenario: An API consumer submitting a request without an accept header         receives a successful response

**Given** the API consumer does not provide an accept header
<br/>
**When** the request is submitted
<br/>
**Then** the response returned is successful
<br/>

**Asserts**
- Response returns a 201 success

**Accept Headers**

This test uses accept header values. Below is a list of acceptable accept header values available to be used with this API.

| Request Header Value             | Response Header Value            |
|----------------------------------|----------------------------------|
| Accept: application/vnd.api+json | Accept: application/vnd.api+json |
| Accept: \*/\*                    | Accept: application/vnd.api+json |
| Accept: application/json         | Accept: application/json         |

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

## Invalid content type


### Scenario: An API consumer submitting a request with an invalid         content type header receives a 415 'Unsupported Media' response

**Given** the API consumer provides an invalid content type header
<br/>
**When** the request is submitted
<br/>
**Then** the response is a 415 unsupported media error
<br/>

**Asserts**
- Response returns a 415 ‘Unsupported Media’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Content Type Headers**

This test uses content-type header values. The api accepts header values insensitive of the case used, however, content-type headers must be in an acceptable format to be accepted and generate a successful response.

| Value        | Description     |
|--------------|-----------------|
| content-type | “”              |
| content-type | application/xml |
| content-type | image/png       |
| content-type | text/plain      |
| content-type | audio/mpeg      |
| content-type | xyz/abc         |
| CONTENT_TYPE | “”              |
| CONTENT_TYPE | application/xml |
| CONTENT_TYPE | image/png       |
| CONTENT_TYPE | text/plain      |
| CONTENT_TYPE | audio/mpeg      |
| CONTENT_TYPE | xyz/abc         |
| Content_Type | “”              |
| Content_Type | application/xml |
| Content_Type | image/png       |
| Content_Type | text/plain      |
| Content_Type | audio/mpeg      |
| Content_Type | xyz/abc         |
| conTENT_tYpe | “”              |
| conTENT_tYpe | application/xml |
| conTENT_tYpe | image/png       |
| conTENT_tYpe | text/plain      |
| conTENT_tYpe | audio/mpeg      |
| conTENT_tYpe | xyz/abc         |

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

## Content negotiation


### Scenario: An API consumer submitting a request with a valid accept header         receives a response containing the expected accept header

**Given** the API consumer provides a valid accept header
<br/>
**When** the request is submitted
<br/>
**Then** the response returned is in the format requested
<br/>

**Asserts**
- Response returns the expected accept header

**Accept Headers**

This test uses accept header values. Below is a list of acceptable accept header values available to be used with this API.

| Request Header Value             | Response Header Value            |
|----------------------------------|----------------------------------|
| Accept: application/vnd.api+json | Accept: application/vnd.api+json |
| Accept: \*/\*                    | Accept: application/vnd.api+json |
| Accept: application/json         | Accept: application/json         |

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
