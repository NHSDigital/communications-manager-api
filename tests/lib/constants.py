CORS_METHODS = "GET, PUT, POST, PATCH, DELETE"
CORS_MAX_AGE = "3628800"
CORS_ALLOW_HEADERS = "origin, x-requested-with, accept, " \
                     "content-type, nhsd-session-urid, " \
                     "x-correlation-id, authorization"
CORS_EXPOSE_HEADERS = "x-correlation-id"


class Error():
    def __init__(self, id, status, title, detail):
        self.id = id
        self.status = status
        self.title = title
        self.detail = detail
        self.links = {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        }


# invalid value constants
ERROR_INVALID_VALUE = Error(
    "CM_INVALID_VALUE",
    "400",
    "Invalid value",
    "The property at the specified location does not allow this value."
)

# missing value constants
ERROR_MISSING_VALUE = Error(
    "CM_MISSING_VALUE",
    "400",
    "Missing property",
    "The property at the specified location is required, but was not present in the request."
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

# not acceptable
ERROR_NOT_ACCEPTABLE = Error(
    "CM_NOT_ACCEPTABLE",
    "406",
    "Not acceptable",
    "This service can only generate application/vnd.api+json or application/json."
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

# not found
ERROR_NOT_FOUND = Error(
    "CM_NOT_FOUND",
    "404",
    "Resource not found",
    "The resource at the requested URI was not found."
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

# service timeout
ERROR_SERVICE_TIMEOUT = Error(
    "CM_TIMEOUT",
    "504",
    "Unable to call service",
    "The downstream service has not responded within the configured timeout period."
)
