"""Locust file"""

import json
from locust import HttpLocust, TaskSet, task


class BookingActions(TaskSet):
    """Booking Actions."""

    auth_token = ''
    flight_id = ''

    def on_start(self):
        """Method to run on start."""
        response = self.client.post('/users/login/', {
            'email': 'testuser@gmail.com',
            'password': 'Password@123'
        })
        token = json.loads(response.text)['data']['token']
        self.auth_token = token

        flight_response = self.client.get(
            '/flights/', headers={'Authorization': 'Bearer ' + token})
        flight_id = json.loads(flight_response.text)['data'][0]['id']
        self.flight_id = flight_id

    @task(1)
    def get_profile(self):
        """Task to get user profile."""
        self.client.get('/users/profile',
                        headers={'Authorization': 'Bearer ' + self.auth_token})

    @task(2)
    def get_bookings(self):
        """task to get bookings"""
        self.client.get('/bookings/ticket/',
                        headers={'Authorization': 'Bearer ' + self.auth_token})

    @task(3)
    def get_reservations(self):
        """task to get bookings"""
        self.client.get('/bookings/reservations/',
                        headers={'Authorization': 'Bearer ' + self.auth_token})

    @task(4)
    def make_bookings(self):
        """task to get bookings"""
        self.client.post(
            '/bookings/ticket/', {
                "seat_number": "BUS-001",
                "type": "BUS",
                "flight": self.flight_id
            },
            headers={'Authorization': 'Bearer ' + self.auth_token})

    @task(5)
    def make_reservations(self):
        """task to get bookings"""
        self.client.post(
            '/bookings/reservations/', {
                "seat_number": "BUS-003",
                "type": "ECO",
                "flight": self.flight_id
            },
            headers={'Authorization': 'Bearer ' + self.auth_token})


class ApplicationUser(HttpLocust):
    """Locust analyze."""

    task_set = BookingActions
    min_wait = 1000
    max_wait = 1000
    host = "https://airtech-v.herokuapp.com/v1"
