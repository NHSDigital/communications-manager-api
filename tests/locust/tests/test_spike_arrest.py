from locust import HttpUser, task, constant, LoadTestShape, TaskSet


class UserTasks(TaskSet):
    @task
    def hit_endpoint(self):
        self.client.get("/_ping")


class SpikeArrestUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]


class OverSpikeArrestLoadShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 99, "spawn_rate": 3, "user_classes": [SpikeArrestUser]},
        {"duration": 120, "users": 110, "spawn_rate": 10, "user_classes": [SpikeArrestUser]},
        {"duration": 180, "users": 80, "spawn_rate": 20, "user_classes": [SpikeArrestUser]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
