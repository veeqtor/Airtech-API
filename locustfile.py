"""Locust file"""

import json
from locust import HttpLocust, TaskSet, task


class BookingActions(TaskSet):
    """Booking Actions."""

    auth_token = ''

    def on_start(self):
        """Method to run on start."""
        response = self.client.post('/users/login/', {
            'email': 'testuser@gmail.com',
            'password': 'Password@123'
        })
        token = json.loads(response.text)['data']['token']
        self.auth_token = token

    @task
    def get_profile(self):
        """Task to get user profile."""
        self.client.get('/users/profile',
                        headers={'Authorization': 'Bearer ' + self.auth_token})


class ApplicationUser(HttpLocust):
    """Locust analyze."""

    task_set = BookingActions
    min_wait = 0
    max_wait = 0
    host = "http://127.0.0.1:9000/v1"
