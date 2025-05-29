Scenario: An API consumer submitting a request with a non-string email address receives a 400 'Invalid Value' response
======================================================================================================================

A valid email contact detail must be structured in this format: { email: Value } where Value is a string

| **Given** the API consumer provides a message body with a non-string email address
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body with references to the invalid attribute

.. list-table::
    :widths: 50 50
    :header-rows: 1

    * - Value
      - Description
    * - []
      - Used to ensure only a string email address is accepted

