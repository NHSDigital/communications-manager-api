**Correlation IDs**

This test uses the 'X-Correlation-Id' header, when provided in a request it is returned in the response.

.. list-table::
    :widths: 50 50
    :header-rows: 1

    * - Value
      - Description
    * - None
      - Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request.
    * - 76491414-d0cf-4655-ae20-a4d1368472f3
      - Is tested to ensure that when a correlation identifier is sent, we respond with the same value.