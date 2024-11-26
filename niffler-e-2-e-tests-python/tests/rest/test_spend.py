import allure

from marks import TestData
from fixtures.client_fixtures import spends_client

from models.enums import Category, Spend
from models.spend import Spend as SpendResponse
from http import HTTPStatus


@allure.tag("API")
@allure.epic("Spending")
class TestSpend:
    @TestData.category(Category.SCHOOL)
    def test_add_spending(self, category, spends_client, remove_all_spends):
        with allure.step('Add spending'):
            response = spends_client.add_spends(Spend.TEST_DATA)
        with allure.step('Assert status code 201'):
            assert response.status_code == HTTPStatus.CREATED
        with allure.step('Validate spend model'):
            SpendResponse.model_validate(response.json())

    @TestData.category(Category.SCHOOL)
    @TestData.spends(Spend.TEST_DATA)
    def test_get_spending(self, category, spends, spends_client, remove_all_spends):
        with allure.step('Get spending'):
            response = spends_client.get_spends()
        with allure.step('Assert status code 200'):
            assert response.status_code == HTTPStatus.OK
        spend_data = response.json()
        with allure.step('Assert that only one spend in list'):
            assert len(spend_data) == 1
        with allure.step('Validate spend model'):
            SpendResponse.model_validate(spend_data[0])

    @TestData.category(Category.SCHOOL)
    @TestData.spends(Spend.TEST_DATA)
    def test_remove_spending(self, category, spends, spends_client):
        response = spends_client.get_spends().json()
        with allure.step('Assert that only one spend in list'):
            assert len(response) == 1
        with allure.step('Remove spending'):
            removed_spend = spends_client.remove_spends(response[0]['id'])
        with allure.step('Assert status code 200'):
            assert removed_spend.status_code == HTTPStatus.OK
        with allure.step('Assert empty list of spendings'):
            spends = spends_client.get_spends()
            assert spends.json() == []
