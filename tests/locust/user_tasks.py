from locust import HttpUser, TaskSet, task, constant, LoadTestShape
import uuid  # for generating unique IDs


class UserTasks(TaskSet):
    @task
    def hit_endpoint(self):
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'X-Correlation-Id': str(uuid.uuid4())  # Generating a unique correlation ID
        }
        data = {
            "data": {
                "type": "MessageBatch",
                "attributes": {}
            }
        }

        with self.client.post(
            url="/v1/message-batches",
            headers=headers,
            json=data,
            catch_response=True
        ) as response:
            if response.status_code <= 400:
                response.success()
