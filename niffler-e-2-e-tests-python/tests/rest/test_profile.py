import allure

from fixtures.client_fixtures import spends_client
from marks import TestData
from models.enums import Category as enum_category
from models.category import Category
from http import HTTPStatus



@allure.story("Profile")
def test_add_new_category(spends_client, category_in_db, remove_all_categories):
    with allure.step('Create category'):
        category = spends_client.add_category(enum_category.SCHOOL)
    with allure.step('Assert status_code 200'):
        assert category.status_code == HTTPStatus.OK
    with allure.step('Validate category model'):
        Category.model_validate(category.json())
    with allure.step('Assert category in database'):
        assert category_in_db(enum_category.SCHOOL) == enum_category.SCHOOL


@TestData.category(enum_category.SCHOOL)
@allure.story("Profile")
def test_add_existing_category(category, spends_client):
    with allure.step('Create category exists'):
        category = spends_client.add_category(enum_category.SCHOOL)
    with allure.step('Assert status code 500'):
        assert category.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@allure.story("Profile")
def test_create_category_over_limits(app_user, setup_categories, spends_client, remove_all_categories):
    username, _ = app_user
    with allure.step('Create category over limits'):
        category = spends_client.add_category('OVER LIMITS')
    with allure.step('Assert status code 406'):
        assert category.status_code == HTTPStatus.NOT_ACCEPTABLE
    with allure.step('Assert details about over limits'):
        assert category.json()['detail'] == f"Can`t add over than 8 categories for user: '{username}'"




