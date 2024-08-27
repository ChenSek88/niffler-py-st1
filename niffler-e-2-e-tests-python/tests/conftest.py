import json
import os
import dotenv
import pytest
import requests
from selene import browser
from faker import Faker

from clients.spends_client import SpendsHttpClient
from pages.main_page import main_page
from pages.login_page import login_page
import requests


fake = Faker()


@pytest.fixture(autouse=True, scope="session")
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def front_url(envs):
    return os.getenv("FRONTEND_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def app_user():
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


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


@pytest.fixture()
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
def registration(front_url, user_for_reg):
    cookie = requests.get(f"{front_url}:9000/register").headers['x-xsrf-token']
    username, password = user_for_reg
    user_data = {"_csrf": cookie, "username": username, "password": password, "passwordSubmit": password}
    user = requests.post(f"{front_url}:9000/register",
        data=user_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': f'XSRF-TOKEN={cookie}'}
    )
    return username, password



@pytest.fixture()
def spends_client(gateway_url, login_app_user) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, login_app_user)


@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["category"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture(params=[])
def spends(request, spends_client):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend["id"] in [spend["id"] for spend in all_spends]:
        spends_client.remove_spends([test_spend["id"]])


@pytest.fixture()
def remove_all_spends(request, spends_client):
    yield
    all_spends = spends_client.get_spends()
    for spend in all_spends:
        spends_client.remove_spends([spend["id"]])


@pytest.fixture()
def spending_page(login_app_user, front_url):
    browser.open(front_url)
