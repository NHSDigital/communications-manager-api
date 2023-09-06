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
        {"duration": 60, "users": 1, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 120, "users": 2, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 180, "users": 3, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 240, "users": 4, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 300, "users": 5, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 360, "users": 6, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 420, "users": 7, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 480, "users": 8, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 540, "users": 9, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 600, "users": 10, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 660, "users": 11, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 720, "users": 12, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 780, "users": 13, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 840, "users": 14, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 900, "users": 15, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 960, "users": 16, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1020, "users": 17, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1080, "users": 18, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1140, "users": 19, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1200, "users": 20, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1260, "users": 21, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1320, "users": 22, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1380, "users": 23, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1440, "users": 24, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1500, "users": 25, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1560, "users": 26, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1620, "users": 27, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1680, "users": 28, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1740, "users": 29, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1800, "users": 30, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1860, "users": 31, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1920, "users": 32, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 1980, "users": 33, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2040, "users": 34, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2100, "users": 35, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2160, "users": 36, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2220, "users": 37, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2280, "users": 38, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2340, "users": 39, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2400, "users": 40, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2460, "users": 41, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2520, "users": 42, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2580, "users": 43, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2640, "users": 44, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2700, "users": 45, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2760, "users": 46, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2820, "users": 47, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2880, "users": 48, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 2940, "users": 49, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3000, "users": 50, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3060, "users": 51, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3120, "users": 52, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3180, "users": 53, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3240, "users": 54, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3300, "users": 55, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3360, "users": 56, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3420, "users": 57, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3480, "users": 58, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3540, "users": 59, "spawn_rate": 0.05, "user_classes": [ApiUser]},
        {"duration": 3600, "users": 60, "spawn_rate": 0.05, "user_classes": [ApiUser]},

    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
