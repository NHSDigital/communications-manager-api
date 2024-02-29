import requests
import time
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib import Error_Handler


class Helper():
    @staticmethod
    def send_single_message(url, auth, body):
        resp = requests.post(f"{url}{MESSAGES_ENDPOINT}", headers={
                **auth,
                "Accept": "application/vnd.api+json",
                "Content-Type": "application/vnd.api+json"
            }, json=body
        )
        Error_Handler.handle_retry(resp)
        assert resp.status_code == 201
        return resp

    @staticmethod
    def get_message(url, auth, message_id):
        resp = requests.get(f"{url}{MESSAGES_ENDPOINT}/{message_id}", headers={
            **auth,
            "Accept": "application/vnd.api+json"
        })
        Error_Handler.handle_retry(resp)
        assert resp.status_code == 200
        return resp

    @staticmethod
    def poll_get_message(url, auth, message_id, end_state="delivered", poll_time=300):
        message_status = None
        end_time = int(time.time()) + poll_time

        while message_status != end_state and int(time.time()) < end_time:
            get_message_response = requests.get(
                f"{url}{MESSAGES_ENDPOINT}/{message_id}",
                headers={
                    **auth,
                    "Accept": "application/vnd.api+json"
                },
            )

            if get_message_response.status_code == 200:
                message_status = get_message_response.json().get("data").get("attributes").get("messageStatus")
            time.sleep(10)

            if message_status == "failed":
                raise ValueError(f"Request ended up in an unexpected state. \
                                 Message status: {message_status}, Message ID: {message_id}")

        if message_status != end_state:
            raise TimeoutError(f"Request took too long to be processed. \
                               Message status: {message_status}, Message ID: {message_id}")
