Scenario: An API consumer submitting a request with an invalid personalisation receives a 400 'Invalid value' response
======================================================================================================================

A valid personalisation must be structured in this format: { parameter: value }

| **Given** the API consumer provides a message body with an invalid personalisation
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
    * - None
      - Are tested to ensure that null personalisation values are not accepted
    * - 5, "", "some-string", []
      - Are tested to ensure that invalid personalisation values are not accepted

