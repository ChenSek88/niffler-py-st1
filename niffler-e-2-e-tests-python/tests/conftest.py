import os
import dotenv
import pytest
from selene import browser, have
from faker import Faker
from pages.main_page import MainPage
from pages.login_page import LoginPage


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
    login_page = LoginPage()
    login_page.login(username, password)


@pytest.fixture()
def logout():
    yield
    browser.element(MainPage.logout).click()


@pytest.fixture
def user_for_reg():
    username = fake.first_name()
    password = fake.password(length=10)
    return username, password