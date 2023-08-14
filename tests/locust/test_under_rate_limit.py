import time
from locust import HttpUser, task, constant, LoadTestShape


class TestUnderLimit(HttpUser):
    wait_time = constant(1)

    @task
    def hit_endpoint(self):
        self.client.get("/_ping")


class HighVolumeLoadShape(LoadTestShape):

    wait_time = constant(0.1)
    stages = [
        {"duration": 180, "users": 200, "spawn_rate": 20, "wait_time": 0.1},
        {"duration": 240, "users": 20, "spawn_rate": 10, "wait_time": 0.5},
        {"duration": 300, "users": 100, "spawn_rate": 2, "wait_time": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
