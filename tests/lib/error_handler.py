import lib.constants as constants


class Error_Handler():
    @staticmethod
    def handle_retry(resp):
        Error_Handler.handle_429_retry(resp)
        Error_Handler.handle_504_retry(resp)

    @staticmethod
    def handle_429_retry(resp):
        if resp.status_code == 429:
            raise constants.UNEXPECTED_429

    @staticmethod
    def handle_504_retry(resp):
        if resp.status_code == 504:
            raise constants.UNEXPECTED_504
