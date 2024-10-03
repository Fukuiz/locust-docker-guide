from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks
    host = "http://your-api.com"  # Replace with your target API URL

    @task
    def get_example(self):
        """Perform a GET request to the /example endpoint."""
        self.client.get("/example")  # Replace with your desired GET endpoint

    @task
    def post_data(self):
        """Perform a POST request to the /data endpoint."""
        self.client.post("/data", json={"key": "value"})  # Replace with your desired POST endpoint and data

    @task
    def put_data(self):
        """Perform a PUT request to the /data/1 endpoint."""
        self.client.put("/data/1", json={"key": "updated_value"})  # Replace with your desired PUT endpoint and data

    @task
    def delete_data(self):
        """Perform a DELETE request to the /data/1 endpoint."""
        self.client.delete("/data/1")  # Replace with your desired DELETE endpoint

