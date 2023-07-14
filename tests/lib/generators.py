from .constants import *


class Generators():
    @staticmethod
    def generate_invalid_value_error(pointer):
        return Generators.generate_error(ERROR_INVALID_VALUE, {
            "pointer": pointer
        })

    @staticmethod
    def generate_missing_value_error(pointer):
        return Generators.generate_error(ERROR_MISSING_VALUE, {
            "pointer": pointer
        })

    @staticmethod
    def generate_null_value_error(pointer):
        return Generators.generate_error(ERROR_NULL_VALUE, {
            "pointer": pointer
        })

    @staticmethod
    def generate_duplicate_value_error(pointer):
        return Generators.generate_error(ERROR_DUPLICATE_VALUE, {
            "pointer": pointer
        })

    @staticmethod
    def generate_too_few_items_error(pointer):
        return Generators.generate_error(ERROR_TOO_FEW_ITEMS, {
            "pointer": pointer
        })

    @staticmethod
    def generate_access_denied_error():
        return Generators.generate_error(ERROR_ACCESS_DENIED, {
            "header": "Authorization"
        })

    @staticmethod
    def generate_forbidden_error():
        return Generators.generate_error(ERROR_FORBIDDEN, {
            "header": "Authorization"
        })

    @staticmethod
    def generate_not_acceptable_error():
        return Generators.generate_error(ERROR_NOT_ACCEPTABLE, {
            "header": "Accept"
        })

    @staticmethod
    def generate_unsupported_media_error():
        return Generators.generate_error(ERROR_UNSUPPORTED_MEDIA, {
            "header": "Content-Type"
        })

    @staticmethod
    def generate_no_such_routing_plan_error():
        return Generators.generate_error(ERROR_NO_SUCH_ROUTING_PLAN, {
            "pointer": "/data/attributes/routingPlanId"
        })

    @staticmethod
    def generate_not_found_error():
        return Generators.generate_error(ERROR_NOT_FOUND, None)

    @staticmethod
    def generate_quota_error():
        return Generators.generate_error(ERROR_QUOTA, None)

    @staticmethod
    def generate_request_timeout_error():
        return Generators.generate_error(ERROR_REQUEST_TIMEOUT, None)

    @staticmethod
    def generate_service_timeout_error():
        return Generators.generate_error(ERROR_SERVICE_TIMEOUT, None)

    @staticmethod
    def generate_error(error, source):
        ret = {
            "id": error.id,
            "links": error.links,
            "status": error.status,
            "title": error.title,
            "detail": error.detail
        }

        if source:
            ret["source"] = source

        return ret
