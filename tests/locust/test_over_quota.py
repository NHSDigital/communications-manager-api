from locust import HttpUser, task, constant, LoadTestShape, TaskSet


class UserTasks(TaskSet):
    @task
    def hit_endpoint(self):
        with self.client.get("/_ping", catch_response=True) as response:
            if response.status_code == 200:
                pass
            elif response.status_code == 429:
                response.success("Expected 429 error returned")
            else:
                response.failure("Unexpected status returned: ", response.status_code)


class QuotaUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]
    host = "https://internal-dev-sandbox.api.service.nhs.uk/comms"


class OverQuotaLoadShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 30, "spawn_rate": 20, "user_classes": [QuotaUser]},
        {"duration": 120, "users": 90, "spawn_rate": 30, "user_classes": [QuotaUser]},
        {"duration": 240, "users": 30, "spawn_rate": 10, "user_classes": [QuotaUser]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
