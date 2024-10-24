import requests
from models.config import Envs
from utils.sessions import BaseSession


class FriendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def friend_request(self, username: str):
        response = self.session.post("/api/invitations/send", json={
            "username": username
        })
        return response.json()
