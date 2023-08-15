from locust import HttpUser, TaskSet, task, constant, LoadTestShape


class UserTasks(TaskSet):
    @task
    def hit_endpoint(self):
        with self.client.get("/_ping", catch_response=True) as response:
            if response.status_code == "200":
                pass
            elif response.status_code == "429":
                response.failure("Unexpected 429 error returned")
            else:
                response.failure("Unexpected status returned: ", response.status_code)


class ApiUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 20, "spawn_rate": 20, "wait_time": 1, "user_classes": [ApiUser]},
        {"duration": 120, "users": 60, "spawn_rate": 30, "wait_time": 1, "user_classes": [ApiUser]},
        {"duration": 240, "users": 49, "spawn_rate": 33, "wait_time": 1, "user_classes": [ApiUser]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
