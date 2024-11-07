import requests


from models.config import Envs
from utils.sessions import BaseSession


class UserRegistrationHTTPClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs):
        self.session = BaseSession(base_url=f"{envs.frontend_url}:9000")
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def get_csrf_token(self):
        response = self.session.get("/register")
        return response.headers['x-xsrf-token']

    def register_user(self, username: str, password: str):
        csrf_token = self.get_csrf_token()
        self.session.cookies.set('XSRF-TOKEN', csrf_token)
        user_data = {
            "_csrf": csrf_token,
            "username": username,
            "password": password,
            "passwordSubmit": password
        }

        response = self.session.post("/register", data=user_data)
        return response
