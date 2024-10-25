import uuid
import lib.constants.constants as constants
from lib.constants.shared_paths import ROUTING_PLAN_ID_PATH


class Generators():
    @staticmethod
    def generate_valid_create_message_batch_body(environment="sandbox"):
        routing_plan_id = constants.VALID_ROUTING_PLAN_ID_SANDBOX

        if environment == "int":
            routing_plan_id = constants.VALID_ROUTING_PLAN_ID_INT
        elif environment == "prod":
            routing_plan_id = constants.VALID_ROUTING_PLAN_ID_PROD
        elif environment == "dev":
            routing_plan_id = constants.VALID_ROUTING_PLAN_ID_DEV

        return {
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": routing_plan_id,
                    "messageBatchReference": str(uuid.uuid1()),
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "9990548609",
                                "dateOfBirth": "2023-01-01"
                            },
                            "originator": {
                                "odsCode": "X26"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }

    @staticmethod
    def generate_valid_create_message_body(environment="sandbox"):
        routing_plan_id = constants.VALID_ROUTING_PLAN_ID_SANDBOX

        if environment == "int":
            routing_plan_id = constants.VALID_ROUTING_PLAN_ID_INT
        elif environment == "prod":
            routing_plan_id = constants.VALID_ROUTING_PLAN_ID_PROD
        elif environment == "dev":
            routing_plan_id = constants.VALID_ROUTING_PLAN_ID_DEV

        return {
            "data": {
                "type": "Message",
                "attributes": {
                    "routingPlanId": routing_plan_id,
                    "messageReference": str(uuid.uuid1()),
                    "recipient": {
                        "nhsNumber": "9990548609",
                        "dateOfBirth": "2023-01-01"
                    },
                    "originator": {
                        "odsCode": "X26"
                    },
                    "personalisation": {}
                }
            }
        }

    @staticmethod
    def generate_send_message_body(channel, environment, personalisation="Hello"):
        if environment == "internal-dev":
            nhs_number = "9627193232"
            date_of_birth = "1998-03-21"
            if channel == "nhsapp":
                nhs_number = "9842434109"
                date_of_birth = "2002-10-23"
        elif environment == "internal-qa":
            nhs_number = "9730617953"
            date_of_birth = "2009-09-02"
        else:
            raise ValueError(f"Invalid environment value provided: {environment}")
        if channel == "nhsapp":
            routing_plan_id = constants.NHS_APP_ROUTING_PLAN
        elif channel == "email":
            routing_plan_id = constants.EMAIL_ROUTING_PLAN
        elif channel == "sms":
            routing_plan_id = constants.SMS_ROUTING_PLAN
        elif channel == "letter":
            routing_plan_id = constants.LETTER_ROUTING_PLAN
        else:
            raise ValueError(f"Invalid channel value provided: {channel}")
        return {
            "data": {
                "type": "Message",
                "attributes": {
                    "routingPlanId": routing_plan_id,
                    "messageReference": str(uuid.uuid1()),
                    "recipient": {
                        "nhsNumber": nhs_number,
                        "dateOfBirth": date_of_birth
                    },
                    "originator": {
                        "odsCode": "X26"
                    },
                    "personalisation": {
                        "exampleParameter": personalisation
                    }
                }
            }
        }

    @staticmethod
    def generate_invalid_value_error(pointer):
        return Generators.generate_error(constants.ERROR_INVALID_VALUE, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_invalid_value_error_custom_detail(pointer, detail):
        return Generators.generate_error_with_custom_detail(constants.ERROR_INVALID_VALUE, detail, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_invalid_nhs_number_error(pointer):
        return Generators.generate_error(constants.ERROR_INVALID_NHS_NUMBER, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_missing_value_error(pointer):
        return Generators.generate_error(constants.ERROR_MISSING_VALUE, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_missing_value_error_custom_detail(pointer, detail):
        return Generators.generate_error_with_custom_detail(constants.ERROR_MISSING_VALUE, detail, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_null_value_error(pointer):
        return Generators.generate_error(constants.ERROR_NULL_VALUE, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_duplicate_value_error(pointer):
        return Generators.generate_error(constants.ERROR_DUPLICATE_VALUE, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_too_few_items_error(pointer):
        return Generators.generate_error(constants.ERROR_TOO_FEW_ITEMS, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_too_few_items_error_custom_detail(pointer, detail):
        return Generators.generate_error_with_custom_detail(constants.ERROR_TOO_FEW_ITEMS, detail, source={
            "pointer": pointer
        })

    @staticmethod
    def generate_access_denied_error():
        return Generators.generate_error(constants.ERROR_ACCESS_DENIED, source={
            "header": "Authorization"
        })

    @staticmethod
    def generate_forbidden_error():
        return Generators.generate_error(constants.ERROR_FORBIDDEN, source={
            "header": "Authorization"
        })

    @staticmethod
    def generate_service_ban_error():
        return Generators.generate_error(constants.ERROR_SERVICE_BAN, source={
            "header": "Authorization"
        })

    @staticmethod
    def generate_not_acceptable_error():
        return Generators.generate_error(constants.ERROR_NOT_ACCEPTABLE, source={
            "header": "Accept"
        })

    @staticmethod
    def generate_unsupported_media_error():
        return Generators.generate_error(constants.ERROR_UNSUPPORTED_MEDIA, source={
            "header": "Content-Type"
        })

    @staticmethod
    def generate_no_such_routing_plan_error():
        return Generators.generate_error(constants.ERROR_NO_SUCH_ROUTING_PLAN, source={
            "pointer": ROUTING_PLAN_ID_PATH
        })

    @staticmethod
    def generate_missing_routing_plan_template_error():
        return Generators.generate_error(constants.ERROR_MISSING_ROUTING_PLAN_TEMPLATE, source={
            "pointer": ROUTING_PLAN_ID_PATH
        })

    @staticmethod
    def generate_not_found_error():
        return Generators.generate_error(constants.ERROR_NOT_FOUND)

    @staticmethod
    def generate_not_allowed_error():
        return Generators.generate_error(constants.ERROR_NOT_ALLOWED)

    @staticmethod
    def generate_quota_error():
        return Generators.generate_error(constants.ERROR_QUOTA)

    @staticmethod
    def generate_quota_error_custom(detail):
        error = constants.ERROR_QUOTA
        error.detail = detail
        return Generators.generate_error(error)

    @staticmethod
    def generate_retry_too_early_error():
        return Generators.generate_error(constants.ERROR_RETRY_TOO_EARLY)

    @staticmethod
    def generate_request_timeout_error():
        return Generators.generate_error(constants.ERROR_REQUEST_TIMEOUT)

    @staticmethod
    def generate_service_unavailable_error():
        return Generators.generate_error(constants.ERROR_SERVICE_UNAVAILABLE)

    @staticmethod
    def generate_service_timeout_error():
        return Generators.generate_error(constants.ERROR_SERVICE_TIMEOUT)

    @staticmethod
    def generate_internal_server_error():
        return Generators.generate_error(constants.ERROR_INTERNAL_SERVER)

    @staticmethod
    def generate_bad_gateway_error():
        return Generators.generate_error(constants.ERROR_BAD_GATEWAY)

    @staticmethod
    def generate_invalid_personalisation_error(detail, pointer):
        return Generators.generate_error(
                constants.ERROR_INVALID_PERSONALISATION,
                detail=detail,
                source={
                    "pointer": pointer
                    })

    @staticmethod
    def generate_error(error, source=None, meta=None, detail=None):
        ret = {
            "code": error.code,
            "links": error.links,
            "status": error.status,
            "title": error.title,
            "detail": detail or error.detail
        }

        if source:
            ret["source"] = source

        if meta:
            ret["meta"] = meta
        return ret

    @staticmethod
    def generate_error_with_custom_detail(error, detail=None, source=None, meta=None):
        ret = {
            "code": error.code,
            "links": error.links,
            "status": error.status,
            "title": error.title,
            "detail": detail or error.detail
        }

        if source:
            ret["source"] = source

        if meta:
            ret["meta"] = meta
        return ret
