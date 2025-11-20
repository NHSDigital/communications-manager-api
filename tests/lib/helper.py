import requests
import time
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib import error_handler

DEFAULT_CONTENT_TYPE = "application/vnd.api+json"


class Helper():
    @staticmethod
    def get_message(url, headers, message_id):
        resp = requests.get(f"{url}{MESSAGES_ENDPOINT}/{message_id}", headers=headers)
        error_handler.handle_retry(resp)
        assert resp.status_code == 200
        return resp

    @staticmethod
    def poll_get_message(url, headers, message_id, end_state="delivered", poll_time=300):
        message_status = None
        end_time = int(time.time()) + poll_time

        while message_status != end_state and int(time.time()) < end_time:
            get_message_response = requests.get(
                f"{url}{MESSAGES_ENDPOINT}/{message_id}",
                headers=headers,
            )

            if get_message_response.status_code == 200:
                message_status = get_message_response.json().get("data").get("attributes").get("messageStatus")
            time.sleep(10)

        if message_status != end_state:
            raise TimeoutError(f"Request took too long to be processed. \
                               Message status: {message_status}, Message ID: {message_id}")
