INT_URL = "https://int.api.service.nhs.uk/comms"
PROD_URL = "https://api.service.nhs.uk/comms"
VALID_ENDPOINTS = ["/v1/message-batches", "/v1/messages", "/v1/api/send", "/v1/messages/1234"]
CORS_METHODS = "GET, PUT, POST, PATCH, DELETE"
CORS_MAX_AGE = "3628800"
CORS_ALLOW_HEADERS = "origin, x-requested-with, accept, " \
                     "content-type, nhsd-session-urid, " \
                     "x-correlation-id, authorization"
CORS_EXPOSE_HEADERS = "x-correlation-id"
CORS_POLICY = "cross-origin"

GLOBAL_ROUTING_CONFIGURATION_NHSAPP = "00000000-0000-0000-0000-000000000001"
GLOBAL_ROUTING_CONFIGURATION_EMAIL = "00000000-0000-0000-0000-000000000002"
GLOBAL_ROUTING_CONFIGURATION_SMS = "00000000-0000-0000-0000-000000000003"

VALID_ROUTING_PLAN_ID_PROD = "00000000-0000-0000-0000-000000000001"
VALID_ROUTING_PLAN_ID_SANDBOX = "b838b13c-f98c-4def-93f0-515d4e4f4ee1"
VALID_ROUTING_PLAN_ID_INT = "119bdd50-783c-4161-a765-792785e46851"
VALID_ROUTING_PLAN_ID_DEV = "0e38317f-1670-480a-9aa9-b711fb136610"

INVALID_ROUTING_PLAN = "ae0f772e-6660-4829-8f11-1ed8a3fc68c2"
INVALID_ROUTING_PLAN_PROD = "acd3d4b9-de96-49ef-9ab9-8ce03e678082"

DUPLICATE_ROUTING_PLAN_TEMPLATE_ID = "bb454d66-033b-45c0-bbb6-d9b3420a0bd4"

MISSING_TEMPLATE_ROUTING_PLANS = [
    "191b5bf4-1a69-4798-ba8e-fbbd7dc3dea2",
    "d66ace32-20c2-4aff-a1fc-9ffa3f9fa577"
]

NHS_APP_ROUTING_PLAN = "db0f0498-d331-4fd9-a460-4d2a2a95b416"
EMAIL_ROUTING_PLAN = "f757f27b-63ee-4059-ba94-571c41e99807"
SMS_ROUTING_PLAN = "83686da4-06c8-4cf2-aebe-abe1857fb750"
LETTER_ROUTING_PLAN = "e5edd3db-503e-4997-b870-88ac9215cb47"

METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
CORRELATION_ID = ["76491414-d0cf-4655-ae20-a4d1368472f3"]
CORRELATION_IDS = [None] + CORRELATION_ID
ORIGIN = "https://my.website"
NUM_MAX_ERRORS = 100
DEV_API_GATEWAY_URL = "https://comms-apim.internal-dev.communications.national.nhs.uk"
INT_API_GATEWAY_URL = "https://comms-apim.int.communications.national.nhs.uk"
PROD_API_GATEWAY_URL = "https://comms-apim.prod.communications.national.nhs.uk"
UAT_API_GATEWAY_URL = "https://comms-apim.uat.communications.national.nhs.uk"
DEFAULT_CONTENT_TYPE = "application/vnd.api+json"

VALID_ACCEPT_HEADERS = ["*/*", DEFAULT_CONTENT_TYPE]
VALID_CONTENT_TYPE_HEADERS = [DEFAULT_CONTENT_TYPE]

INVALID_MESSAGE_VALUES = ["", [], 5, 0.1]

INVALID_NHS_NUMBER = ["999054860", "99905486090", "abcdefghij", "", [], {}, 5, 0.1]
# Set to PDS production smoke test user
VALID_NHS_NUMBER = "9990548609"

INVALID_PERSONALISATION_VALUES = [5, "", "some-string", []]
NULL_VALUES = [None]


class Error():
    def __init__(self, code, status, title, detail, links={}):
        self.code = code
        self.status = status
        self.title = title
        self.detail = detail
        self.links = {
            **{"about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify"},
            **links
        }


# invalid value constants
ERROR_INVALID_VALUE = Error(
    "CM_INVALID_VALUE",
    "400",
    "Invalid value",
    "The property at the specified location does not allow this value."
)

# invalid nhs number constants
ERROR_INVALID_NHS_NUMBER = Error(
    "CM_INVALID_NHS_NUMBER",
    "400",
    "Invalid nhs number",
    "The value provided in this nhsNumber field is not a valid NHS number.",
    {"nhsNumbers": "https://www.datadictionary.nhs.uk/attributes/nhs_number.html"}
)

# missing odsCode constants
ERROR_MISSING_ODS_CODE = Error(
    "CM_ODS_CODE_REQUIRED",
    "400",
    "Originator odsCode must be provided",
    "An originator with odsCode must be provided, as your account does not have a default ODS code."
)

# missing value constants
ERROR_MISSING_VALUE = Error(
    "CM_MISSING_VALUE",
    "400",
    "Missing property",
    "The property at the specified location is required, but was not present in the request."
)

# too few address lines
ERROR_TOO_FEW_ADDRESS_LINES = Error(
    "CM_MISSING_VALUE",
    "400",
    "Missing value",
    "Too few address lines were provided"
)

# null value constants
ERROR_NULL_VALUE = Error(
    "CM_NULL_VALUE",
    "400",
    "Property cannot be null",
    "The property at the specified location is required, but a null value was "
    "passed in the request."
)

# duplicate value constants
ERROR_DUPLICATE_VALUE = Error(
    "CM_DUPLICATE_VALUE",
    "400",
    "Duplicate value",
    "The property at the specified location is a duplicate, duplicated values "
    "are not allowed."
)

# too few items constants
ERROR_TOO_FEW_ITEMS = Error(
    "CM_TOO_FEW_ITEMS",
    "400",
    "Too few items",
    "The property at the specified location contains too few items."
)

# access denied
ERROR_ACCESS_DENIED = Error(
    "CM_DENIED",
    "401",
    "Access denied",
    "Access token missing, invalid or expired, "
    "or calling application not configured for "
    "this operation."
)

# forbidden
ERROR_FORBIDDEN = Error(
    "CM_FORBIDDEN",
    "403",
    "Forbidden",
    "Client not recognised or not yet onboarded."
)

# service ban
ERROR_SERVICE_BAN = Error(
    "CM_SERVICE_BAN",
    "403",
    "Service ban in effect",
    "A service ban is in effect on your account."
)

# not acceptable
ERROR_NOT_ACCEPTABLE = Error(
    "CM_NOT_ACCEPTABLE",
    "406",
    "Not acceptable",
    "This service can only generate application/vnd.api+json or application/json."
)

# request too large
ERROR_TOO_LARGE = Error(
    "CM_TOO_LARGE",
    "413",
    "Request too large",
    "Request message was larger than the service limit"
)

ERROR_TOO_MANY_ITEMS = Error(
    "CM_TOO_MANY_ITEMS",
    "413",
    "Too many items",
    "The property at the specified location contains too many items."
)

# unsupported media
ERROR_UNSUPPORTED_MEDIA = Error(
    "CM_UNSUPPORTED_MEDIA",
    "415",
    "Unsupported media",
    "Invalid content-type, this API only "
    "supports application/vnd.api+json or "
    "application/json."
)

# no such routing plan
ERROR_NO_SUCH_ROUTING_PLAN = Error(
    "CM_NO_SUCH_ROUTING_PLAN",
    "404",
    "No such routing plan",
    "The routing plan specified either does not exist or is not in a usable state."
)

# missing routing plan
ERROR_MISSING_ROUTING_PLAN_TEMPLATE = Error(
    "CM_MISSING_ROUTING_PLAN_TEMPLATE",
    "500",
    "Templates missing",
    "The templates required to use the routing plan were not found."
)

# not found
ERROR_NOT_FOUND = Error(
    "CM_NOT_FOUND",
    "404",
    "Resource not found",
    "The resource at the requested URI was not found."
)

# not allowed
ERROR_NOT_ALLOWED = Error(
    "CM_NOT_ALLOWED",
    "405",
    "Method not allowed",
    "The method at the requested URI was not allowed."
)

# retry too early
ERROR_RETRY_TOO_EARLY = Error(
    "CM_RETRY_TOO_EARLY",
    "425",
    "Retried too early",
    "You have retried this request too early, the previous "
    "request is still being processed. Re-send the request "
    "after the time (in seconds) specified `Retry-After` header."
)

# over quota
ERROR_QUOTA = Error(
    "CM_QUOTA",
    "429",
    "Too many requests",
    "You have made too many requests. "
    "Re-send the request after the time (in seconds) "
    "specified `Retry-After` header."
)

# request timeout
ERROR_REQUEST_TIMEOUT = Error(
    "CM_TIMEOUT",
    "408",
    "Request timeout",
    "The service was unable to receive your request within the timeout period."
)

# service unavailable
ERROR_SERVICE_UNAVAILABLE = Error(
    "CM_SERVICE_UNAVAILABLE",
    "503",
    "The service is currently unavailable",
    "The service is currently not able to process this request, try again later."
)

# service timeout
ERROR_SERVICE_TIMEOUT = Error(
    "CM_TIMEOUT",
    "504",
    "Unable to call service",
    "The downstream service has not responded within the configured timeout period."
)

# internal server error
ERROR_INTERNAL_SERVER = Error(
    "CM_INTERNAL_SERVER_ERROR",
    "500",
    "Error processing request",
    "There was an internal error whilst processing this request."
)

# bad gateway error
ERROR_BAD_GATEWAY = Error(
    "CM_BAD_GATEWAY",
    "502",
    "Unable to call service",
    "A downstream service is not responding."
)

# invalid personalisation error
ERROR_INVALID_PERSONALISATION = Error(
    "CM_INVALID_VALUE",
    "400",
    "Invalid personalisation",
    ""
)

INVALID_REQUEST_TITLE = "Invalid Request"

# NHS App Accounts errors
ERROR_NHS_APP_ACCOUNTS_MISSING_ODS_CODE = Error(
    "CM_INVALID_REQUEST",
    "400",
    INVALID_REQUEST_TITLE,
    "Missing ODS Code"
)

ERROR_NHS_APP_ACCOUNTS_INVALID_ODS_CODE = Error(
    "CM_INVALID_REQUEST",
    "400",
    INVALID_REQUEST_TITLE,
    "Invalid ODS Code"
)

ERROR_NHS_APP_ACCOUNTS_INVALID_PAGE = Error(
    "CM_INVALID_REQUEST",
    "400",
    INVALID_REQUEST_TITLE,
    "page must be a positive non-zero integer"
)

ERROR_NHS_APP_ACCOUNTS_REPORT_NOT_FOUND = Error(
    "CM_NOT_FOUND",
    "404",
    "Resource not found",
    "Report not found"
)

ERROR_NHS_APP_ACCOUNTS_TOO_MANY_REQUESTS = Error(
    "CM_QUOTA",
    "429",
    "Too many requests",
    "This endpoint is currently receiving a high volume of requests and is being rate limited."
)

ERROR_CANNOT_SET_CONTACT_DETAILS = Error(
    "CM_CANNOT_SET_CONTACT_DETAILS",
    "400",
    "Cannot set contact details",
    "Client is not allowed to provide alternative contact details."
)

ERROR_DUPLICATE_MESSAGE_REQUEST = Error(
    "CM_DUPLICATE_REQUEST",
    "422",
    "Duplicate message request",
    "Request exists with identical messageReference"
)

ERROR_DUPLICATE_BATCH_REQUEST = Error(
    "CM_DUPLICATE_REQUEST",
    "422",
    "Duplicate batch request",
    "Request exists with identical messageBatchReference"
)
