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
