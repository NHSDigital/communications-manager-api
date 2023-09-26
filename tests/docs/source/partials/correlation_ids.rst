.. list-table:: Correlation Ids
    :widths: 50 50
    :header-rows: 1

    * - Value
      - Description
    * - None
      - Is tested to ensure that we do not send back a correlation identifier if the user has not provided one.
    * - 76491414-d0cf-4655-ae20-a4d1368472f3
      - Is tested to ensure that when the user sends a correlation identifier, we respond with the same value.