from locust import HttpUser, task, constant, LoadTestShape, TaskSet


class UserTasks(TaskSet):
    @task
    def hit_endpoint(self):
        self.client.get("/_ping")


class QuotaUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]


class OverQuotaLoadShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 15, "spawn_rate": 20, "user_classes": [QuotaUser]},
        {"duration": 120, "users": 20, "spawn_rate": 30, "user_classes": [QuotaUser]},
        {"duration": 180, "users": 5, "spawn_rate": 10, "user_classes": [QuotaUser]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
