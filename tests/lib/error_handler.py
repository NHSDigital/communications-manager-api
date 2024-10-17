import lib.constants.constants as constants

codes_to_retry = [401, 429, 504]


class error_handler():
    @staticmethod
    def handle_retry(resp, excluded_code=None):
        for code_to_retry in codes_to_retry:
            if code_to_retry != excluded_code and code_to_retry == resp.status_code:
                raise AssertionError(f'Unexpected {code_to_retry}')
