import json
import os
import dotenv
import pytest
import requests
from selene import browser
from faker import Faker
from pages.main_page import main_page
from pages.login_page import login_page
import requests


fake = Faker()


@pytest.fixture(autouse=True, scope="session")
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def front_url():
    return os.getenv("FRONT_URL")


@pytest.fixture(scope="session")
def test_user():
    return os.getenv("TEST_USER"), os.getenv("TEST_PASSWORD")


@pytest.fixture()
def login_test_user(test_user):
    username, password = test_user
    login_page.login(username, password)


@pytest.fixture()
def logout():
    yield
    browser.element(main_page.logout).click()


@pytest.fixture()
def user_for_reg():
    username = fake.first_name()
    password = fake.password(length=10)
    return username, password


@pytest.fixture()
def update_profile_data():
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