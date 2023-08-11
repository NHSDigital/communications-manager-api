import time
from locust import HttpUser, task, TaskSet


class TestRateLimit(HttpUser):
    wait_time = time.sleep

    @task
    def hit_endpoint(self):
        self.client.options("https://internal-dev-sandbox.api.service.nhs.uk/comms/_ping")
