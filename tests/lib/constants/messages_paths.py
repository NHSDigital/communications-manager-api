
from lib.constants.shared_paths import ROUTING_PLAN_ID_PATH

MESSAGES_ENDPOINT = "/v1/messages"
MESSAGE_REFERENCE_PATH = "/data/attributes/messageReference"
MESSAGE_RECIPIENT_PATH = "/data/attributes/recipient"
MESSAGE_RECIPIENT_NHSNUMBER_PATH = "/data/attributes/recipient/nhsNumber"
MESSAGE_PERSONALISATION_PATH = "/data/attributes/personalisation"

MISSING_PROPERTIES_PATHS = [
    ("data", "/data"),
    ("type", "/data/type"),
    ("attributes", "/data/attributes"),
    ("routingPlanId", ROUTING_PLAN_ID_PATH),
    ("messageReference", MESSAGE_REFERENCE_PATH),
    ("recipient", MESSAGE_RECIPIENT_PATH),
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
    ("personalisation", MESSAGE_PERSONALISATION_PATH),
]

MESSAGE_IDS = [
    "pending_enrichment_request_item_id",
    "pending_enrichment_single_request_item_id",
    "cascade_sending_all_status_request_item_id",
    "conditionally_overridden_routing_config_request_item_id",
    "contact_missing_email_request_item_id",
    "contact_missing_email_single_request_item_id",
    "contact_missing_sms_request_item_id",
    "contact_missing_sms_single_request_item_id",
    "contact_missing_letter_request_item_id",
    "contact_missing_letter_single_request_item_id",
    "contact_missing_nhsapp_request_item_id",
    "contact_missing_nhsapp_single_request_item_id",
    "successful_email_request_item_id",
    "successful_sms_request_item_id",
    "successful_sms_single_request_item_id",
    "successful_letter_request_item_id",
    "successful_letter_single_request_item_id",
    "successful_nhsapp_request_item_id",
    "successful_nhsapp_single_request_item_id",
    "sending_email_request_item_id",
    "sending_email_single_request_item_id",
    "sending_sms_request_item_id",
    "sending_sms_single_request_item_id",
    "sending_letter_request_item_id",
    "sending_letter_single_request_item_id",
    "sending_nhsapp_request_item_id",
    "sending_nhsapp_single_request_item_id",
    "no_pds_request_item_id",
    "no_pds_single_request_item_id",
    "invalidated_record_request_item_id",
    "invalidated_record_single_request_item_id",
    "dob_mismatch_request_item_id",
    "dob_mismatch_single_request_item_id",
    "formally_dead_request_item_id",
    "formally_dead_single_request_item_id",
    "informally_dead_request_item_id",
    "informally_dead_single_request_item_id",
    "exit_code_request_item_id",
    "exit_code_single_request_item_id",
    "pds_name_error_request_item_id",
    "pds_name_error_single_request_item_id"
]

SINGLE_MESSAGE_ID = "2aUxQER3co3kXdvTKrhbSFHRRxR"
BATCH_MESSAGE_ID = "2aUxdGDkW87biAvPOfG8ATYHj00"
MESSAGE_ID_NOT_BELONGING_TO_CLIENT = "2aUx0TuRORU8yXX7MPNoEUtGVg3"

SUCCESSFUL_MESSAGE_IDS = [
    SINGLE_MESSAGE_ID,
    BATCH_MESSAGE_ID
]

CHANNEL_TYPE = [
        "nhsapp",
        "email",
        "sms",
        "letter"
    ]
CHANNEL_STATUS = [
        "created",
        "sending",
        "delivered",
        "failed",
        "skipped"
    ]
