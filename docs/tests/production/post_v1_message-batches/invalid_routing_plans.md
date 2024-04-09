# Invalid Routing Plans


..py:function:: test_no_such_routing_plan

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


## Scenario: An API consumer submitting a request with a routing plan routing plan not associated with their client ID receives a 404 ‘No Such Routing Plan’ response

**Given** the API consumer provides a routing plan not associated with their client ID
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
