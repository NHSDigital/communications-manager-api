# Invalid Routing Plans


## Scenario: An API consumer submitting a request with a routing plan referencing the same template twice receives a 500 ‘Duplicate Routing Plan’ response

**Given** the API consumer provides a message body containing a reference to the same template twice
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 500 duplicate routing plan error
<br/>

**Asserts**
- Response returns a 500 ‘Duplicate Routing Plan’ error
- Response returns the expected error message body referencing the duplicate template values
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


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
