import lib.constants.constants as constants

codes_to_retry = [401, 429, 504, 502]


class error_handler():
    @staticmethod
    def handle_retry(resp):
        if resp.status_code in codes_to_retry:
            raise AssertionError(f'Unexpected {resp.status_code}')
