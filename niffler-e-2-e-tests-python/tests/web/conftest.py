import pytest
from faker import Faker

from pages.main_page import main_page
from pages.login_page import login_page
import requests
from http import HTTPStatus
from conftest import envs
from _pytest.fixtures import FixtureRequest


pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures"]


@pytest.fixture(scope="session")
def app_user(envs):
    return envs.test_username, envs.test_password.get_secret_value()


@pytest.fixture()
def login_app_user(app_user):
    username, password = app_user
    login_page.login(username, password)


@pytest.fixture()
def logout():
    yield
    main_page.logout()


fake = Faker()


@pytest.fixture()
def user_for_reg(user_db):
    username = fake.first_name()
    password = fake.password(length=10)
    yield username, password
    user_db.delete_user_authority(username)
    user_db.delete_user(username)


@pytest.fixture()
def profile_data():
    name = fake.first_name()
    surname = fake.last_name()
    return name, surname


@pytest.fixture()
def registration(envs, user_for_reg, user_db, userdata_db):
    cookie = requests.get(f"{envs.frontend_url}:9000/register").headers['x-xsrf-token']
    username, password = user_for_reg
    user_data = {"_csrf": cookie, "username": username, "password": password, "passwordSubmit": password}
    response = requests.post(f"{envs.frontend_url}:9000/register",
        data=user_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': f'XSRF-TOKEN={cookie}'}
    )
    assert response.status_code == HTTPStatus.CREATED
    yield username, password
    userdata_db.delete_friend_request(username)
    userdata_db.delete_userdata(username)
    user_db.delete_user_authority(username)
    user_db.delete_user(username)


@pytest.fixture()
def friend_request(friends_client, userdata_db):
    def add_friend(username):
        friends_client.friend_request(username)
    yield add_friend


@pytest.fixture()
def user_in_db(user_db):
    def get_username_from_db(username: str):
        user = user_db.get_user(username)
        return user.username if user else print(f'Username: {username} not found')
    return get_username_from_db


@pytest.fixture()
def delete_user(user_db, userdata_db):
    def delete(username):
        userdata_db.delete_friend_request(username)
        userdata_db.delete_userdata(username)
        user_db.delete_user_authority(username)
        user_db.delete_user(username)
    return delete


@pytest.fixture()
def category_in_db(spend_db):
    def get_category_from_db(category_name):
        category = spend_db.get_category(category_name)
        return category.category if category else print(f'Category: {category_name} not found')
    return get_category_from_db


@pytest.fixture()
def firstname_surname_in_db(userdata_db):
    def get_firstname_surname_from_db(username):
        user_profile = userdata_db.get_user_profile(username)
        return user_profile.firstname, user_profile.surname
    return get_firstname_surname_from_db


@pytest.fixture(params=[])
def category(request: FixtureRequest, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


@pytest.fixture()
def remove_all_spends(request: FixtureRequest, spends_client):
    yield
    all_spends = spends_client.get_spends()
    for spend in all_spends:
        spends_client.remove_spends([spend.id])


@pytest.fixture()
def remove_all_categories(request: FixtureRequest, spends_client, spend_db):
    yield
    categories = spends_client.get_categories()
    for category in categories:
        spend_db.delete_category(category.id)
