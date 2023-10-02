import uuid
import lib.constants as constants


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
                            "personalisation": {}
                        }
                    ]
                }
            }
        }

    @staticmethod
    def generate_invalid_value_error(pointer):
        return Generators.generate_error(constants.ERROR_INVALID_VALUE, source={
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
            "pointer": constants.ROUTING_PLAN_ID_PATH
        })

    @staticmethod
    def generate_missing_routing_plan_template_error():
        return Generators.generate_error(constants.ERROR_MISSING_ROUTING_PLAN_TEMPLATE, source={
            "pointer": constants.ROUTING_PLAN_ID_PATH
        })

    @staticmethod
    def generate_duplicate_routing_plan_template_error(expectedDuplicates):
        return Generators.generate_error(
            constants.ERROR_DUPLICATE_ROUTING_PLAN_TEMPLATE,
            source={
                "pointer": constants.ROUTING_PLAN_ID_PATH
            },
            meta={
                "duplicateTemplates": expectedDuplicates
            }
        )

    @staticmethod
    def generate_not_found_error():
        return Generators.generate_error(constants.ERROR_NOT_FOUND)

    @staticmethod
    def generate_quota_error():
        return Generators.generate_error(constants.ERROR_QUOTA)

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
    def generate_error(error, source=None, meta=None):
        ret = {
            "code": error.code,
            "links": error.links,
            "status": error.status,
            "title": error.title,
            "detail": error.detail
        }

        if source:
            ret["source"] = source

        if meta:
            ret["meta"] = meta
        return ret
