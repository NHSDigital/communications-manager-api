from lib.constants.shared_paths import ROUTING_PLAN_ID_PATH


MESSAGE_BATCH_REFERENCE_PATH = "/data/attributes/messageBatchReference"
MESSAGES_PATH = "/data/attributes/messages"
FIRST_MESSAGE_REFERENCE_PATH = "/data/attributes/messages/0/messageReference"
FIRST_MESSAGE_RECIPIENT_PATH = "/data/attributes/messages/0/recipient"
FIRST_MESSAGE_RECIPIENT_NHSNUMBER_PATH = "/data/attributes/messages/0/recipient/nhsNumber"

MISSING_PROPERTIES_PATHS = [
    ("data", "/data"),
    ("type", "/data/type"),
    ("attributes", "/data/attributes"),
    ("routingPlanId", ROUTING_PLAN_ID_PATH),
    ("messageBatchReference", MESSAGE_BATCH_REFERENCE_PATH),
    ("messages", MESSAGES_PATH),
    ("messageReference", FIRST_MESSAGE_REFERENCE_PATH),
    ("recipient", FIRST_MESSAGE_RECIPIENT_PATH),
    ("nhsNumber", FIRST_MESSAGE_RECIPIENT_NHSNUMBER_PATH),
]
NULL_PROPERTIES_PATHS = [
    ("data", "/data"),
    ("attributes", "/data/attributes"),
    ("recipient", FIRST_MESSAGE_RECIPIENT_PATH),
]
INVALID_PROPERTIES_PATHS = [
    ("type", "/data/type"),
    ("routingPlanId", ROUTING_PLAN_ID_PATH),
    ("messageBatchReference", MESSAGE_BATCH_REFERENCE_PATH),
    ("messages", MESSAGES_PATH),
    ("messageReference", FIRST_MESSAGE_REFERENCE_PATH),
    ("recipient", FIRST_MESSAGE_RECIPIENT_PATH),
    ("dateOfBirth", "/data/attributes/messages/0/recipient/dateOfBirth"),
    ("personalisation", "/data/attributes/messages/0/personalisation"),
]
DUPLICATE_PROPERTIES_PATHS = [
    ("messageReference", "/data/attributes/messages/1/messageReference"),
]
TOO_FEW_PROPERTIES_PATHS = [
    ("messages", MESSAGES_PATH),
]
