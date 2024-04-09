# Invalid Routing Plans


## Scenario: An API consumer submitting a request with a routing plan referencing a missing template receives a 500 ‘Missing Routing Plan’ response

**Given** the API consumer provides a message body with a routing plan referencing a missing template
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 500 missing routing plan template error
<br/>

**Asserts**
- Response returns a 500 ‘Missing Routing Plan Template’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


## Scenario: An API consumer submitting a request with an invalid routing plan receives a 400 ‘Invalid Value’ response

**Given** the API consumer provides a message body with a routing plan referencing an invalid template
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body referencing the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


## Scenario: An API consumer submitting a request with an unknown routing plan receives a 404 ‘No Such Routing Plan’ response

**Given** the API consumer provides a message body with an unknown routing plan
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 404 no such routing plan error
<br/>

**Asserts**
- Response returns a 404 ‘No Such Routing Plan’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |
