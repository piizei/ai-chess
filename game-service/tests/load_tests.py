import os

from locust import HttpUser, task, constant
import random


class SvelteLoader(HttpUser):
    wait_time = constant(0)
    # This load test is ran against the sveltekit backend (only publicly exposed service)
    host = os.getenv("HOST", "http://localhost:5173")

    @task
    def test_voting(self):
        # create random string
        random_str = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.client.post("/api/chat",
                         data={"message": random_str},
                         headers={"X-Client-Anon-Guid": random_str})

    @task
    def test_status(self):
        # create random string
        random_str = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.client.get("/api/status",
                        headers={"X-Client-Anon-Guid": random_str})
