from pages.login_page import login_page
from pages.main_page import main_page
from pages.presentation_page import presentation_page
import allure


@allure.tag("WEB")
@allure.epic("Authorization")
class TestLoginPage:
    def test_login_successful(self, app_user):
        user, password = app_user
        login_page.login(user, password)
        main_page.assert_main_page_title('Niffler. The coin keeper.')

    def test_logout(self, login_app_user):
        main_page.logout()
        presentation_page.assert_header_title('Welcome to magic journey with Niffler. The coin keeper')

    def test_invalid_login(self, app_user):
        user, password = app_user
        login_page.login(user, 'bad' + password)
        login_page.assert_bad_login('Bad credentials')
