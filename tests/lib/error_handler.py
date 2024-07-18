import lib.constants.constants as constants


class error_handler():
    @staticmethod
    def handle_retry(resp):
        error_handler.handle_429_retry(resp)
        error_handler.handle_504_retry(resp)

    @staticmethod
    def handle_429_retry(resp):
        if resp.status_code == 429:
            raise constants.UNEXPECTED_429

    @staticmethod
    def handle_504_retry(resp):
        if resp.status_code == 504:
            raise constants.UNEXPECTED_504
