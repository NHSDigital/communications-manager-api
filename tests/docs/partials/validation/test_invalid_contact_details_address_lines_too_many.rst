Scenario: An API consumer submitting a request with invalid address lines (too many) receives a 400 'Invalid Value' response
===============================================================================================================================

A valid contact detail must be structured in this format: { address: { lines: [ Value1, Value2 ], postcode: value } }

| **Given** the API consumer provides an message body with with too many address lines
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid value' error
- Response returns the expected error message body with references to the invalid attribute

.. list-table::
    :widths: 50 50
    :header-rows: 1

    * - Value
      - Description
    * - [ "1", "2", "3", "4", "5", "6" ]
      - Used to ensure list of more than 5 values is not accepted

