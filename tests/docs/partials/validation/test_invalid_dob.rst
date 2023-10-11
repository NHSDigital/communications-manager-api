Scenario: An API consumer submitting a request with an invalid date of birth receives a 400 'Invalid Value' response
====================================================================================================================

A valid date of birth must be structured in this format: YYYY-MM-dd

| **Given** the API consumer provides an message body with an invalid date of birth
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
    * - 1990-10-1, 1990-1-10, 90-10-10
      - Are tested to ensure that date of birth is only accepted in the format YYYY-MM-DD
    * - 10-12-1990, 1-MAY-2000, 1990/01/01
      - Are tested to ensure that date of birth is only accepted as a ISO-8601 format
    * - "", None
      - Are tested to ensure that null date of birth values are not accepted
    * - [], {}, 5, 0.1
      - Are tested to ensure that invalid date of birth values are not accepted

