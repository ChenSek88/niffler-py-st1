import allure
import pytest

from fixtures.client_fixtures import spends_client
from fixtures.client_fixtures import userdata_client
from marks import TestData
from models.enums import Category as EnumsCategory
from models.category import Category
from models.userdata import User as UserData
from http import HTTPStatus


@allure.tag("API")
@allure.epic("Profile")
class TestProfile:
    def test_add_new_category(self, spends_client, spend_db, remove_all_categories):
        with allure.step('Create category'):
            response = spends_client.add_category(EnumsCategory.SCHOOL)
        with allure.step('Assert status_code 200'):
            assert response.status_code == HTTPStatus.OK
        with allure.step('Validate category model'):
            Category.model_validate(response.json())
        with allure.step('Assert category in database'):
            assert spend_db.is_category_in_db(EnumsCategory.SCHOOL)

    @TestData.category(EnumsCategory.SCHOOL)
    @pytest.mark.xfail
    #Баг, при создании существующей категории, сервер возвращает 500
    def test_add_existing_category(self, category, spends_client):
        with allure.step('Create existing category'):
            response = spends_client.add_category(EnumsCategory.SCHOOL)
        with allure.step('Assert status code 400'):
            assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_category_over_limits(self, app_user, add_max_count_categories, spends_client):
        username, _ = app_user
        with allure.step('Create category over limits'):
            response = spends_client.add_category(EnumsCategory.OVER_LIMITS)
        with allure.step('Assert status code 406'):
            assert response.status_code == HTTPStatus.NOT_ACCEPTABLE
        with allure.step('Assert details about over limits'):
            assert response.json()['detail'] == f"Can`t add over than 8 categories for user: '{username}'"

    def test_update_firstname_surname(self, app_user, userdata_client, userdata_db, profile_data):
        username, _ = app_user
        firstname, surname = profile_data
        with allure.step('Update firstname and surname'):
            response = userdata_client.update_userdata('RUB', firstname, surname)
        with allure.step('Assert status_code 200'):
            assert response.status_code == HTTPStatus.OK
        with allure.step('Validate userdata model'):
            UserData.model_validate(response.json())
        with allure.step('Assert firstname and surname in db'):
            assert userdata_db.firstname_surname_in_db(username) == (firstname, surname)

    @TestData.category(EnumsCategory.SCHOOL)
    def test_get_category(self, category, spends_client):
        with allure.step('Get category'):
            response = spends_client.get_categories()
        with allure.step('Assert status_code 200'):
            assert response.status_code == HTTPStatus.OK
        category = response.json()
        with allure.step('Assert that only one category in list'):
            assert len(category) == 1
        with allure.step('Assert category name'):
            assert category[0]['category'] == EnumsCategory.SCHOOL
        with allure.step('Validate category model'):
            Category.model_validate(category[0])

    def test_get_categories(self, add_max_count_categories, spends_client):
        with allure.step('Get categories'):
            response = spends_client.get_categories()
        with allure.step('Assert status_code 200'):
            assert response.status_code == HTTPStatus.OK
        categories = response.json()
        with allure.step('Assert all categories'):
            assert len(categories) == 8
        with allure.step('Validate category model'):
            [Category.model_validate(item) for item in categories]
