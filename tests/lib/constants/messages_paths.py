
from lib.constants.shared_paths import ROUTING_PLAN_ID_PATH


MESSAGE_REFERENCE_PATH = "/data/attributes/messageReference"
MESSAGE_RECIPIENT_PATH = "/data/attributes/recipient"
MESSAGE_RECIPIENT_NHSNUMBER_PATH = "/data/attributes/recipient/nhsNumber"
MESSAGE_RECIPIENT_DOB_PATH = "/data/attributes/recipient/dateOfBirth"
MESSAGE_PERSONALISATION_PATH = "/data/attributes/personalisation"

MISSING_PROPERTIES_PATHS = [
    ("data", "/data"),
    ("type", "/data/type"),
    ("attributes", "/data/attributes"),
    ("routingPlanId", ROUTING_PLAN_ID_PATH),
    ("messageReference", MESSAGE_REFERENCE_PATH),
    ("recipient", MESSAGE_RECIPIENT_PATH),
    ("nhsNumber", MESSAGE_RECIPIENT_NHSNUMBER_PATH),
]
NULL_PROPERTIES_PATHS = [
    ("data", "/data"),
    ("attributes", "/data/attributes"),
    ("recipient", MESSAGE_RECIPIENT_PATH),
]
INVALID_PROPERTIES_PATHS = [
    ("type", "/data/type"),
    ("routingPlanId", ROUTING_PLAN_ID_PATH),
    ("messageReference", MESSAGE_REFERENCE_PATH),
    ("recipient", MESSAGE_RECIPIENT_PATH),
    ("dateOfBirth", MESSAGE_RECIPIENT_DOB_PATH),
    ("personalisation", MESSAGE_PERSONALISATION_PATH),
]
