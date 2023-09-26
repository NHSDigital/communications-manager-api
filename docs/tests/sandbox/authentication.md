# Authentication Tests


### Test 401 responses

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc fermentum finibus eros id pulvinar. Aliquam erat volutpat. Praesent iaculis congue pretium. Nullam consequat at velit ut iaculis. Suspendisse pulvinar tempor ex, id facilisis justo varius sed. Proin pulvinar odio ut dui pulvinar, sed semper neque porttitor. Sed vel faucibus mi. Donec sit amet velit mollis, venenatis erat nec, facilisis tortor. Cras ac eros hendrerit sapien gravida mattis. Duis posuere posuere urna. Nunc vel ornare erat. Cras rhoncus lacus metus, ut facilisis ligula tempor at. Donec ultricies elit ut arcu lacinia consectetur. Integer non lacus luctus, finibus enim eget, mollis erat.

Morbi ut condimentum diam, tempus interdum arcu. Pellentesque est quam, elementum ac aliquet vitae, eleifend sed diam. Donec eleifend gravida justo, sed finibus orci ornare quis. Integer suscipit lacus at suscipit commodo. Mauris vel sodales eros. Cras viverra rutrum sodales. Nullam nec sapien pharetra, viverra lorem sit amet, rutrum nulla. Phasellus sit amet erat eu massa condimentum pellentesque.

Vestibulum tempus velit vitae tellus suscipit, euismod consectetur est mattis. Etiam eget cursus dui. Donec dignissim quis neque sed imperdiet. Etiam a consectetur risus. Donec a est enim. Curabitur ac odio non diam faucibus maximus. Nulla ut magna pulvinar, laoreet nunc non, finibus lectus. Etiam efficitur eleifend lectus, semper interdum magna molestie nec.

Nullam pellentesque ornare leo id rhoncus. Suspendisse varius auctor ex, quis feugiat urna fermentum ut. Nullam tincidunt neque sit amet mi tincidunt tristique. Nulla dignissim massa eget felis bibendum, sed efficitur arcu gravida. Donec semper arcu sed lorem maximus feugiat. In consequat consequat sapien sed consectetur. Vestibulum efficitur, purus a egestas molestie, tortor elit ultricies diam, rutrum lacinia lectus neque eu diam. Fusce vestibulum auctor condimentum. Sed viverra laoreet quam a tempor. In vitae nulla et mauris viverra lacinia vel laoreet turpis. Praesent tortor odio, cursus a porttitor aliquam, molestie eu dui.

Morbi at laoreet justo. Fusce aliquam tellus quam, sit amet aliquam tortor interdum sed. Suspendisse placerat leo et ultrices aliquam. Cras imperdiet, magna ut ullamcorper faucibus, est quam condimentum nunc, sed venenatis elit ipsum in erat. Mauris at velit id ex tempor fringilla vitae et lorem. Nulla facilisi. Maecenas sit amet odio in neque tempus feugiat. Vestibulum accumsan arcu orci, eget aliquet felis venenatis vitae.

* **Parameters:**
  * **nhsd_apim_proxy_url** – The URL of the proxy that the request will be sent to.
  * **correlation_id** – The correlation id value to be sent in the X-Correlation-Id header.
  * **method** – The HTTP method to test.
* **Asserts:**
  Asserts that the request fails with a 401 response code, validating that the error response body is correctly formed.

#### Correlation Ids

| Value                                | Description                                                                                             |
|--------------------------------------|---------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if the user has not provided one. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when the user sends a correlation identifier, we respond with the same value.  |
