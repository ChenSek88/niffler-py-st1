import allure
from marks import TestData
from fixtures.client_fixtures import spends_client

from models.enums import Category
from models.spend import SpendAdd

from http import HTTPStatus


AMOUNT = 50000
DESCRIPTION = "QA-GURU PYTHON ADVANCED"
CURRENCY = 'RUB'


@TestData.category(Category.SCHOOL)
@allure.epic("API")
@allure.story("Spending")
def test_add_spending(category, spends_client, remove_all_spends):
    with allure.step('Add spending'):
        spend_data = SpendAdd(
            amount=AMOUNT,
            description=DESCRIPTION,
            category=Category.SCHOOL,
            spendDate="2024-08-08T18:39:27.955Z",
            currency=CURRENCY
        )
        spends = spends_client.add_spends(spend_data)
    with allure.step('Assert status code 201'):
        assert spends.status_code == HTTPStatus.CREATED
    with allure.step('Validate spend model'):
        SpendAdd.model_validate(spends.json())


@TestData.category(Category.SCHOOL)
@TestData.spends(
    SpendAdd(
        amount=AMOUNT,
        description=DESCRIPTION,
        category=Category.SCHOOL,
        spendDate="2024-08-08T18:39:27.955Z",
        currency=CURRENCY
    )
)
@allure.epic("API")
@allure.story("Spending")
def test_remove_spending(category, spends, spends_client):
    spend = spends_client.get_spends().json()
    with allure.step('Remove spending'):
        removed_spend = spends_client.remove_spends(spend[0]['id'])
    with allure.step('Assert status code 200'):
        assert removed_spend.status_code == HTTPStatus.OK
