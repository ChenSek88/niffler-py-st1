import base64
import hashlib
import os
import re
from urllib.parse import urlparse, parse_qs

from requests import Session

from models.config import Envs


class AuthSession(Session):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.code = None


    def request(self, method, url, **kwargs):
        response = super().request(method, url, **kwargs)
        for r in response.history:
            cookies = r.cookies.get_dict()
            self.cookies.update(cookies)
            code = parse_qs(urlparse(r.headers.get("Location")).query).get("code", None)
            if code:
                self.code = code
        return response


class AuthClient:

    def __init__(self, env: Envs):
        self.session = AuthSession()
        self.domain_url = env.auth_url
        self.frontend_url = env.frontend_url
        self.code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        self.code_verifier = re.sub('[^a-zA-Z0-9]+', '', self.code_verifier)

        self.code_challenge = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        self.code_challenge = base64.urlsafe_b64encode(self.code_challenge).decode('utf-8')
        self.code_challenge = self.code_challenge.replace('=', '')

        self._basic_token = base64.b64encode(env.auth_secret.encode('utf-8')).decode('utf-8')
        self.authorization_basic = {"Authorization": f"Basic {self._basic_token}"}
        self.token = None


    def auth(self, username, password):

        session = AuthSession()

        session.get(
            url=f"{self.domain_url}/oauth2/authorize",
            params={
                "response_type": "code",
                "client_id": "client",
                "scope": "openid",
                "redirect_uri": f"{self.frontend_url}/authorized",
                "code_challenge": self.code_challenge,
                "code_challenge_method": "S256",
            },
            allow_redirects=True
        )

        session.post(
            url=f"{self.domain_url}/login",
            data={
                "username": username,
                "password": password,
                "_csrf": session.cookies.get("XSRF-TOKEN")
            },
            allow_redirects=True
        )

        token_response = session.post(
            url=f"{self.domain_url}/oauth2/token",
            data={
                "code": session.code,
                "redirect_uri": f"{self.frontend_url}/authorized",
                "code_verifier": self.code_verifier,
                "grant_type": "authorization_code",
                "client_id": "client"
            },
            headers=self.authorization_basic,
        )

        self.token = token_response.json().get("access_token", None)
        return self.token
