Scenario: An API consumer submitting a request with an invalid email receives a 400 'Invalid Value' response
======================================================================================================================

A valid contact detail must be structured in this format: { email: Value }

| **Given** the API consumer provides an message body with an invalid email address
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the 'X-Correlation-Id' header if provided

.. list-table::
    :widths: 50 50
    :header-rows: 1

    * - Value
      - Description
    * - invalidEmailAddress
      - Used to ensure invalid email address is not accepted

