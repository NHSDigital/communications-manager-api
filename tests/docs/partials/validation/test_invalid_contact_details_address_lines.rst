Scenario: An API consumer submitting a request with a non-string array address lines receives a 400 'Invalid Value' response
============================================================================================================================

A valid address lines contact detail must be structured in this format: { address: { lines: Value } } where Value is a string array

| **Given** the API consumer provides a message body with a non-string array address lines
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
    * - [1,2]
      - Used to ensure only a string array address lines is accepted

