import requests

from models.config import Envs
from models.spend import SpendAdd
from models.category import Category
from utils.sessions import BaseSession


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def get_categories(self) -> list[Category]:
        return self.session.get("/api/categories/all")

    def add_category(self, name: str):
        category = self.session.post("/api/categories/add", json={
            "category": name
        })
        return category

    def get_spends(self) -> list:
        return self.session.get("/api/spends/all")


    def add_spends(self, spend: SpendAdd):
        return self.session.post("/api/spends/add", json=spend.model_dump())

    def remove_spends(self, ids: list[str]):
        return self.session.delete("/api/spends/remove", params={"ids": ids})
