# Invalid Routing Plans


### Scenario: An API consumer submitting a request with a routing plan         not belonging to the associated client ID receives a 404 'No Such Routing Plan' response

**Given** the API consumer provides a routing plan not associated to a client ID
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 404 no such routing plan error
<br/>

**Asserts**
- Response returns a 404 ‘No Such Routing Plan’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided
.. include:: ../../partials/correlation_ids.rst


### Test using someone elses routing plan
