import allure

from fixtures.client_fixtures import spends_client
from fixtures.client_fixtures import userdata_client
from marks import TestData
from models.enums import Category as EnumsCategory
from models.category import Category
from models.userdata import User as UserData
from http import HTTPStatus

CATEGORY = 'OVER LIMITS'


@allure.epic("API")
@allure.story("Profile")
def test_add_new_category(spends_client, category_in_db, remove_all_categories):
    with allure.step('Create category'):
        category = spends_client.add_category(EnumsCategory.SCHOOL)
    with allure.step('Assert status_code 200'):
        assert category.status_code == HTTPStatus.OK
    with allure.step('Validate category model'):
        Category.model_validate(category.json())
    with allure.step('Assert category in database'):
        assert category_in_db(EnumsCategory.SCHOOL) == EnumsCategory.SCHOOL


@allure.epic("API")
@TestData.category(EnumsCategory.SCHOOL)
@allure.story("Profile")
def test_add_existing_category(category, spends_client):
    with allure.step('Create category exists'):
        category = spends_client.add_category(EnumsCategory.SCHOOL)
    with allure.step('Assert status code 500'):
        assert category.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@allure.epic("API")
@allure.story("Profile")
def test_create_category_over_limits(app_user, add_max_count_categories, spends_client, remove_all_categories):
    username, _ = app_user
    with allure.step('Create category over limits'):
        category = spends_client.add_category(CATEGORY)
    with allure.step('Assert status code 406'):
        assert category.status_code == HTTPStatus.NOT_ACCEPTABLE
    with allure.step('Assert details about over limits'):
        assert category.json()['detail'] == f"Can`t add over than 8 categories for user: '{username}'"


@allure.epic("API")
@allure.story("Profile")
def test_update_firstname_surname(app_user, userdata_client, profile_data, firstname_surname_in_db):
    username, _ = app_user
    firstname, surname = profile_data
    with allure.step('Update firstname and surname'):
        userdata = userdata_client.update_userdata('RUB', firstname, surname)
    with allure.step('Assert status_code 200'):
        assert userdata.status_code == HTTPStatus.OK
    with allure.step('Validate userdata model'):
        UserData.model_validate(userdata.json())
    with allure.step('Assert firstname and surname in db'):
        assert firstname_surname_in_db(username) == (firstname, surname)


@allure.epic("API")
@TestData.category(EnumsCategory.SCHOOL)
@allure.story("Profile")
def test_get_category(category, spends_client):
    with allure.step('Get one category'):
        category = spends_client.get_categories()
    with allure.step('Assert status_code 200'):
        assert category.status_code == HTTPStatus.OK
    with allure.step('Validate category model'):
        [Category.model_validate(item) for item in category.json()]


@allure.epic("API")
@allure.story("Profile")
def test_get_categories(add_max_count_categories, spends_client, remove_all_categories):
    with allure.step('Get categories'):
        category = spends_client.get_categories()
    with allure.step('Assert status_code 200'):
        assert category.status_code == HTTPStatus.OK
    with allure.step('Validate category model'):
        [Category.model_validate(item) for item in category.json()]
