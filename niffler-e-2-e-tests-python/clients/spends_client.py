import requests

from models.config import Envs
from models.spend import Spend, SpendAdd
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
        response = self.session.get("/api/categories/all")
        return [Category.model_validate(item) for item in response.json()]


    def add_category(self, name: str):
        response = self.session.post("/api/categories/add", json={
            "category": name
        })
        return response


    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        return [Spend.model_validate(item) for item in response.json()]


    def add_spends(self, spend: SpendAdd) -> Spend:
        response = self.session.post("/api/spends/add", json=spend.model_dump())
        return Spend.model_validate(response.json())


    def remove_spends(self, ids: list[str]):
        self.session.delete("/api/spends/remove", params={"ids": ids})
