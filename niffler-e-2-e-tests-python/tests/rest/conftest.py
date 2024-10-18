import pytest
from conftest import envs
from faker import Faker
from _pytest.fixtures import FixtureRequest

from models.enums import Category

fake = Faker()


pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures"]


@pytest.fixture(scope="session")
def app_user(envs):
    return envs.test_username, envs.test_password.get_secret_value()


@pytest.fixture()
def user_for_reg(user_db):
    username = fake.first_name()
    password = fake.password(length=10)
    yield username, password
    user_db.delete_user_authority(username)
    user_db.delete_user(username)


@pytest.fixture()
def user_in_db(user_db):
    def get_username_from_db(username: str):
        user = user_db.get_user(username)
        return user.username if user else print(f'Username: {username} not found')
    return get_username_from_db


@pytest.fixture(params=[])
def category(request: FixtureRequest, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.json()['category']
    spend_db.delete_category(category.json()['id'])


@pytest.fixture()
def remove_all_categories(request: FixtureRequest, spends_client, spend_db):
    yield
    categories = spends_client.get_categories()
    for category in categories:
        spend_db.delete_category(category.id)


@pytest.fixture()
def category_in_db(spend_db):
    def get_category_from_db(category_name):
        category = spend_db.get_category(category_name)
        return category.category if category else print(f'Category: {category_name} not found')
    return get_category_from_db


CATEGORIES = [
    Category.SCHOOL,
    Category.INTERNET,
    Category.CARSHARING,
    Category.PHARMACY,
    Category.FAST_FOOD,
    Category.SUPERMARKET,
    Category.TELECOM,
    Category.BANK
]


@pytest.fixture
def setup_categories(spends_client, spend_db):
    created_categories = []
    for category in CATEGORIES:
        created_category = spends_client.add_category(category)
        created_categories.append(created_category)
