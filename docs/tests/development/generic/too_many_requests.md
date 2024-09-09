# Too Many Requests Tests

## 429 - Too Many Requests


### Scenario: An API consumer submitting requests when exceeding the specific app spike arrest rate limit for another app

**Given** A specific app spike arrest rate limit is set for a different app
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is 200 OK
<br/>

**Asserts**
- Response returns a 200 OK
- Response returns the expected message body


### Scenario: An API consumer submitting requests when exceeding the specific app quota rate limit for another app

**Given** A specific app quota rate limit is set for a different app
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is 200 OK
<br/>

**Asserts**
- Response returns a 200 OK
- Response returns the expected message body


### Scenario: An API consumer submitting requests when exceeding the global app quota rate limit

**Given** A global app quota rate limit
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is a 429 Too Many Requests error
<br/>

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting requests when exceeding the global app spike arrest rate limit

**Given** A global app spike arrest rate limit
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is a 429 Too Many Requests error
<br/>

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body


### Scenario: An API consumer submitting requests when exceeding the proxy quota rate limit

**Given** A proxy quota rate limit
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is a 429 Too Many Requests error
<br/>

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body


### Scenario: An API consumer submitting requests when exceeding the proxy spike arrest rate limit

**Given** A proxy spike arrest rate limit
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is a 429 Too Many Requests error
<br/>

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body


### Scenario: An API consumer submitting requests when exceeding the specific app quota rate limit

**Given** A specific app quota rate limit
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is a 429 Too Many Requests error
<br/>

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body


### Scenario: An API consumer submitting requests when exceeding the specific app spike arrest rate limit

**Given** A specific app spike arrest rate limit
<br/>
**When** requests exceeding that limit are submitted
<br/>
**Then** the response is a 429 Too Many Requests error
<br/>

**Asserts**
- Response returns a 429 Too Many Requests error
- Response returns the expected error message body
