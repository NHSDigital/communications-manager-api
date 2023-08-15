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


class SpikeArrestUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]


class OverSpikeArrestLoadShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 99, "spawn_rate": 3, "user_classes": [SpikeArrestUser]},
        {"duration": 120, "users": 110, "spawn_rate": 10, "user_classes": [SpikeArrestUser]},
        {"duration": 240, "users": 80, "spawn_rate": 20, "user_classes": [SpikeArrestUser]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
