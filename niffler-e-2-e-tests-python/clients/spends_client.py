from urllib.parse import urljoin

import requests


class SpendsHttpClient:

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

    def get_categories(self):
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        response.raise_for_status()
        return response.json()

    def add_category(self, name: str):
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={
            "category": name
        })
        response.raise_for_status()
        return response.json()

    def add_spends(self, body):
        url = urljoin(self.base_url, "/api/spends/add")
        response = self.session.post(url, json=body)
        response.raise_for_status()
        return response.json()

    def get_spends(self):
        url = urljoin(self.base_url, "/api/spends/all")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def remove_spends(self, ids: list[int]):
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids})
        response.raise_for_status()