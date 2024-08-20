from pages.registration_page import registration_page
from pages.login_page import login_page
from pages.main_page import main_page


def test_registration_successful(user_for_reg, logout):
        username, password = user_for_reg
        registration_page.user_registration(username, password)
        login_page.login(username, password)
        main_page.assert_main_page_title('Niffler. The coin keeper.')


def test_registration_with_diff_passwords(user_for_reg):
        username, password = user_for_reg
        registration_page.registration_with_diff_passwords(username, password)
        registration_page.assert_bad_registration('Passwords should be equal')


def test_registration_an_existing_user(registration):
        username, password = registration
        registration_page.user_registration(username, password)
        registration_page.assert_bad_registration(f'Username `{username}` already exists')