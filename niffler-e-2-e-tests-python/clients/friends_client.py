from urllib.parse import urljoin

import requests

class FriendsHttpClient:

    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })


    def friend_request(self, username: str):
        request = self.session.post(urljoin(self.base_url, "/api/invitations/send"), json={
            "username": username
        })
        request.raise_for_status()
        return request.json()
