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
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": str(uuid.uuid4()),  # Generating a unique message batch reference
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "9990548609",
                                "dateOfBirth": "1932-01-06"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
        self.client.post(
            url="/v1/message-batches",
            headers=headers,
            json=data
        )
