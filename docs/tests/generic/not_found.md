# Not Found Tests

## 404 - Not Found


### Scenario: An API consumer submitting a request to an unknown endpoint receives a 404 ‘Not Found’ response

**Given** the API consumer does not know how to identify the resource they want to fetch
<br/>
**When** the request is submitted to an unknown resource
<br/>
**Then** the service responds with a 404 not found response, telling the user the resource does not exist
<br/>

**Asserts**
- Response returns a 404 ‘Not Found’ error
- Response returns the expected error message body

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
