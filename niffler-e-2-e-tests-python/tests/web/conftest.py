import pytest

from pages.main_page import main_page
from pages.login_page import login_page
import requests
from http import HTTPStatus
from conftest import envs
from selene.support.shared import browser as shared_browser


pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.database_fixtures", "fixtures.generate_data_fixtures"]


@pytest.fixture(scope='function', autouse=True)
def browser_setup(envs):
    shared_browser.config.browser_name = 'chrome'
    shared_browser.open(envs.frontend_url)
    shared_browser.driver.maximize_window()
    yield
    shared_browser.quit()


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
