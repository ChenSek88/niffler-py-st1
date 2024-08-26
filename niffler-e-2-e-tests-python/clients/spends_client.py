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
        categories = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        categories.raise_for_status()
        return categories.json()

    def add_category(self, name: str):
        category = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={
            "category": name
        })
        category.raise_for_status()
        return category.json()

    def add_spends(self, body):
        url = urljoin(self.base_url, "/api/spends/add")
        spends = self.session.post(url, json=body)
        spends.raise_for_status()
        return spends.json()

    def get_spends(self):
        url = urljoin(self.base_url, "/api/spends/all")
        all_spends = self.session.get(url)
        all_spends.raise_for_status()
        return all_spends.json()

    def remove_spends(self, ids: list[int]):
        url = urljoin(self.base_url, "/api/spends/remove")
        spends = self.session.delete(url, params={"ids": ids})
        spends.raise_for_status()