from pages.registration_page import registration_page
from pages.login_page import login_page
from pages.main_page import main_page
import allure


@allure.story("Registration")
def test_registration_successful(user_for_reg, user_in_db, logout):
    username, password = user_for_reg
    registration_page.user_registration(username, password)
    assert user_in_db(username) == username
    login_page.login(username, password)
    main_page.assert_main_page_title('Niffler. The coin keeper.')


@allure.story("Registration")
def test_registration_with_diff_passwords(user_for_reg):
    username, password = user_for_reg
    registration_page.registration_with_diff_passwords(username, password)
    registration_page.assert_bad_registration('Passwords should be equal')


@allure.story("Registration")
def test_registration_an_existing_user(app_user):
    username, password = app_user
    registration_page.user_registration(username, password)
    registration_page.assert_bad_registration(f'Username `{username}` already exists')
