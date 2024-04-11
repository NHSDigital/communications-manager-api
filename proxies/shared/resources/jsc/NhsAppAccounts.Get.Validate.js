/**
 * This script validates GET requests to the channels/nhsapp/accounts endpoint
 * array of up to 100 error responses to be returned by Apigee as a 400 error response.
 *
 * It is called by the JavaScript.NhsAppAccounts.Get.Validate policy.
 */


var queryParamsList = request.queryParams;
var errors = [];

const odsCodeParamName = "ods-organisation-code";
const odsCodeParamPointer = "queryParam." + odsCodeParamName;

if (queryParamsList.includes(odsCodeParamName)) {
  var odsCode = context.getVariable("request.queryparam." + odsCodeParamName);

  validateOdsCode(errors, odsCode, odsCodeParamPointer);
} else {
  errors.push(missingError(odsCodeParamPointer));
}

if (errors.length > 0) {
    context.setVariable("errors", JSON.stringify(errors));
} else {
    context.setVariable("errors", null);
}
