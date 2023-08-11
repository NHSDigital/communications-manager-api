import time
from locust import HttpUser, task, constant


class TestRateLimit(HttpUser):
    wait_time = constant(1)
    host = "https://internal-dev-sandbox.api.service.nhs.uk/comms"

    @task
    def hit_endpoint(self):
        self.client.get("/_ping")
