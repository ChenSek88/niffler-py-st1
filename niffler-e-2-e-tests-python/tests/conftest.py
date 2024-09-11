import os

from dotenv import load_dotenv
import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import Item, FixtureDef, FixtureRequest
from selene import browser
from faker import Faker

from clients.spends_client import SpendsHttpClient
from clients.friends_client import FriendsHttpClient
from pages.main_page import main_page
from pages.login_page import login_page
import requests
from databases.spend_db import SpendDb
from databases.user_db import UserDb
from databases.userdata_db import UserDataDb
from models.config import Envs



def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs_instance =  Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        user_db_url=os.getenv("USER_DB_URL"),
        userdata_db_url=os.getenv("USERDATA_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


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
    allure.attach(id_token, name="token.txt", attachment_type=AttachmentType.TEXT)
    return id_token


@pytest.fixture()
def logout():
    yield
    main_page.logout()


fake = Faker()


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
def friends_client(envs, login_app_user) -> FriendsHttpClient:
    return FriendsHttpClient(envs.gateway_url, login_app_user)


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
    userdata_db.delete_friend_request(username)
    userdata_db.delete_userdata(username)


@pytest.fixture()
def friend_request(friends_client, userdata_db):
    def add_friend(username):
        friends_client.friend_request(username)
    yield add_friend


@pytest.fixture
def delete_user(user_db, userdata_db):
    def delete(username):
        userdata_db.delete_friend_request(username)
        userdata_db.delete_userdata(username)
        user_db.delete_user_authority(username)
        user_db.delete_user(username)
    return delete


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


@pytest.fixture()
def spending_page(login_app_user, envs):
    browser.open(envs.frontend_url)

