from pages.login_page import login_page
from pages.main_page import main_page
from pages.presentation_page import presentation_page
import allure


@allure.epic("WEB")
@allure.story("Authorization")
def test_login_successful(app_user):
    user, password = app_user
    login_page.login(user, password)
    main_page.assert_main_page_title('Niffler. The coin keeper.')


@allure.epic("WEB")
@allure.story("Authorization")
def test_logout(login_app_user):
    main_page.logout()
    presentation_page.assert_header_title('Welcome to magic journey with Niffler. The coin keeper')


@allure.epic("WEB")
@allure.story("Authorization")
def test_invalid_login(app_user):
    user, password = app_user
    login_page.login(user, 'bad' + password)
    login_page.assert_bad_login('Bad credentials')
