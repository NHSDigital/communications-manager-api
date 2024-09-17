Scenario: An API consumer submitting a request with invalid address lines (too few) receives a 400 'Too few items' response
============================================================================================================================

A valid contact detail must be structured in this format: { address: { lines: [ Value1, Value2 ], postcode: value } }

| **Given** the API consumer provides an message body with with too few address lines
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Too few items' error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the 'X-Correlation-Id' header if provided

.. list-table::
    :widths: 50 50
    :header-rows: 1

    * - Value
      - Description
    * - [ "1" ]
      - Used to ensure list of less than 2 values is not accepted

