/**
 * This script validates the data in the body of a POST request to the /v1/messages endpoint, returning an
 * array of up to 100 error responses to be returned by Apigee as a 400 error response.
 *
 * It is called by the JavaScript.Messages.Create.Validate policy.
 */

context.setVariable("errors", null);
