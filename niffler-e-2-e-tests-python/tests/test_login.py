from pages.login_page import login_page
from pages.main_page import main_page
import allure


@allure.story("Authorization")


def test_login_successful(app_user, logout):
    user, password = app_user
    login_page.login(user, password)
    main_page.assert_main_page_title('Niffler. The coin keeper.')


@allure.story("Authorization")
def test_invalid_login(app_user):
    user, password = app_user
    login_page.login(user, 'bad' + password)
    login_page.assert_bad_login('Bad credentials')
