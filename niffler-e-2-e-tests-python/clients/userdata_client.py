import requests

from models.config import Envs
from utils.sessions import BaseSession


class UserdataHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def update_userdata(self, currency: str, firstname: str, surname: str):
        userdata = self.session.post("/api/users/update", json={
            "currency": currency,
            "firstname": firstname,
            "surname": surname
        })
        return userdata