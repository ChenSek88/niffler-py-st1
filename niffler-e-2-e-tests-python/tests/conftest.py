import os
from dotenv import load_dotenv
import pytest
from selene import browser
from faker import Faker

from clients.spends_client import SpendsHttpClient
from pages.main_page import main_page
from pages.login_page import login_page
import requests
from databases.spend_db import SpendDb
from databases.user_db import UserDb
from databases.userdata_db import UserDataDb
from models.config import Envs
from time import sleep


fake = Faker()


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        user_db_url=os.getenv("USER_DB_URL"),
        userdata_db_url=os.getenv("USERDATA_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )


@pytest.fixture(scope="session")
def app_user(envs):
    return envs.test_username, envs.test_password


@pytest.fixture()
def login_app_user(app_user):
    username, password = app_user
    login_page.login(username, password)
    id_token = None
    while id_token is None:
        id_token = browser.execute_script('return window.sessionStorage.getItem("id_token")')
    return id_token


@pytest.fixture()
def logout():
    yield
    main_page.logout()


@pytest.fixture(scope="session")
def user_for_reg():
    username = fake.first_name()
    password = fake.password(length=10)
    return username, password


@pytest.fixture()
def profile_data():
    name = fake.first_name()
    surname = fake.last_name()
    return name, surname


@pytest.fixture()
def spends_client(envs, login_app_user) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, login_app_user)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(scope="session")
def user_db(envs) -> UserDb:
    return UserDb(envs.user_db_url)


@pytest.fixture(scope="session")
def userdata_db(envs) -> UserDataDb:
    return UserDataDb(envs.userdata_db_url)


@pytest.fixture(scope="session")
def registration(envs, user_for_reg, user_db, userdata_db):
    cookie = requests.get(f"{envs.frontend_url}:9000/register").headers['x-xsrf-token']
    username, password = user_for_reg
    user_data = {"_csrf": cookie, "username": username, "password": password, "passwordSubmit": password}
    requests.post(f"{envs.frontend_url}:9000/register",
        data=user_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': f'XSRF-TOKEN={cookie}'}
    )
    yield username, password
    user_db.delete_user_authority(username)
    user_db.delete_user(username)
    # Форма регистрации восстанавливает запись в таблице user (niffler-userdata) после некоторой задержки.
    # Это происходит даже в случае если срабатывает исключение 'Username `{username}` already exists'
    # Если удалить запись с этим пользователем сразу, то она через некоторое время появится снова
    # Возможно это баг
    sleep(5)
    userdata_db.delete_friend_request(username)
    userdata_db.delete_userdata(username)


@pytest.fixture
def delete_user(user_db, userdata_db):
    def delete(username):
        userdata_db.delete_userdata(username)
        user_db.delete_user_authority(username)
        user_db.delete_user(username)
    return delete


@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
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
def remove_all_spends(request, spends_client):
    yield
    all_spends = spends_client.get_spends()
    for spend in all_spends:
        spends_client.remove_spends([spend.id])


@pytest.fixture()
def remove_all_categories(request, spends_client, spend_db):
    yield
    categories = spends_client.get_categories()
    for category in categories:
        spend_db.delete_category(category.id)


@pytest.fixture()
def spending_page(login_app_user, envs):
    browser.open(envs.frontend_url)

