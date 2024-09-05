Scenario: An API consumer submitting a request with an invalid sms receives a 400 'Invalid Value' response
======================================================================================================================

A valid sms contact detail must be structured in this format: { sms: value }

| **Given** the API consumer provides an message body with an invalid sms
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
    * - 077009000021
      - Used to ensure invalid phone number is not accepted

