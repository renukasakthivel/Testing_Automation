import locust
from locust import HttpUser, task, between

class LoginTest(HttpUser):
    host = "http://127.0.0.1:5000"  

    wait_time = between(1, 5)

    @task
    def login(self):
        response = self.client.post("/login", {
            "email": "example1@gmail.com",
            "password": "example1@123"
        })
        
        if response.status_code == 200:
            print("Login successful!")
        else:
            print("Login failed!")
    
    @task
    def home_page(self):
        self.client.get("/")

    @task
    def browse_shop(self):
        self.client.get("/shop")
