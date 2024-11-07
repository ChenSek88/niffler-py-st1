from pages.registration_page import registration_page
from pages.login_page import login_page
from pages.main_page import main_page
import allure


@allure.tag("WEB")
@allure.epic("Registration")
class TestRegistrationPage:
    def test_registration_successful(self, user_for_reg, user_db, delete_user):
        username, password = user_for_reg
        # проброс username в фикстуру, для удаления юзера в teardown
        delete_user.username = username
        registration_page.user_registration(username, password)
        assert user_db.is_user_in_db(username)
        login_page.login(username, password)
        main_page.assert_main_page_title('Niffler. The coin keeper.')

    def test_registration_with_diff_passwords(self, user_for_reg):
        username, password = user_for_reg
        registration_page.registration_with_diff_passwords(username, password)
        registration_page.assert_bad_registration('Passwords should be equal')

    def test_registration_an_existing_user(self, app_user):
        username, password = app_user
        registration_page.user_registration(username, password)
        registration_page.assert_bad_registration(f'Username `{username}` already exists')
