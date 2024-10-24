import allure

from marks import TestData
from fixtures.client_fixtures import spends_client

from models.enums import Category, Spend
from models.spend import SpendAdd, Spend as SpendResponse
from http import HTTPStatus


@allure.epic("API")
@allure.story("Spending")
@TestData.category(Category.SCHOOL)
def test_add_spending(category, spends_client, remove_all_spends):
    with allure.step('Add spending'):
        spends = spends_client.add_spends(Spend.TEST_DATA)
    with allure.step('Assert status code 201'):
        assert spends.status_code == HTTPStatus.CREATED
    with allure.step('Validate spend model'):
        SpendResponse.model_validate(spends.json())


@allure.epic("API")
@allure.story("Spending")
@TestData.category(Category.SCHOOL)
@TestData.spends(Spend.TEST_DATA)
def test_get_spending(category, spends, spends_client, remove_all_spends):
    with allure.step('Get spending'):
        spend = spends_client.get_spends()
    with allure.step('Assert status code 200'):
        assert spend.status_code == HTTPStatus.OK
    with allure.step('Validate spend model'):
        [SpendResponse.model_validate(item) for item in spend.json()]


@allure.epic("API")
@allure.story("Spending")
@TestData.category(Category.SCHOOL)
@TestData.spends(Spend.TEST_DATA)
def test_remove_spending(category, spends, spends_client):
    spend = spends_client.get_spends().json()
    with allure.step('Remove spending'):
        removed_spend = spends_client.remove_spends(spend[0]['id'])
    with allure.step('Assert status code 200'):
        assert removed_spend.status_code == HTTPStatus.OK
    with allure.step('Assert empty list of spendings'):
        spends = spends_client.get_spends()
        assert spends.json() == []
