import csv
import os
import time
import string
import uuid
from locust import HttpUser
from locust import TaskSet
from locust import task
from locust import constant
from locust import LoadTestShape
from locust import between
from tests.lib.authentication import Authentication


class UserTasks(TaskSet):
    @task
    def post_to_api(self):
        # call_time = None
        row = 1
        Bearer_Token = None
        messageBatchReference = str(uuid.uuid1())
        routingPlanId = "119bdd50-783c-4161-a765-792785e46851"
        while True:
            X_Correlation_ID = str(uuid.uuid1())
            messageReference = str(uuid.uuid1())

            data = None
            with open("tests/locust/test_data/pds-data.csv", "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                data = [[c.replace('\ufeff', '') for c in row] for row in reader]

            if data is None:
                return

            # skip first line as it has headers
            for row in range(1, len(data)):
                nhsNumber = data[row][0]
                # dateOfBirth = data[row][1]

                Bearer_Token = Authentication.generate_int_authentication()

                headers = {
                    "accept": "application/vnd.api+json",
                    "X-Correlation-ID": X_Correlation_ID,
                    "Content-Type": "application/vnd.api+json",
                    "Authorization": Bearer_Token
                }

                json = {
                    "data": {
                        "type": "MessageBatch",
                        "attributes": {
                            "routingPlanId": routingPlanId,
                            "messageBatchReference": messageBatchReference,
                            "messages": [
                                {
                                    "messageReference": messageReference,
                                    "recipient": {
                                        "nhsNumber": nhsNumber,
                                        # "dateOfBirth": dateOfBirth
                                    },
                                    "personalisation": {}
                                }
                            ]
                        }
                    }
                }

                self.client.post("/comms/v1/message-batches", json=json, headers=headers)
                print(Bearer_Token)
                time.sleep(8)
                # if row > rowCount:
                break


class ApiUser(HttpUser):
    wait_time = between(1, 10)
    tasks = [UserTasks]


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 600, "users": 1, "spawn_rate": 1, "user_classes": [ApiUser]},
        {"duration": 3000, "users": 2, "spawn_rate": 1, "user_classes": [ApiUser]},
        {"duration": 3600, "users": 1, "spawn_rate": 1, "user_classes": [ApiUser]},

    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
