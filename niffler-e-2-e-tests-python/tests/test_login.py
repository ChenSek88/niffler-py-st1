from pages.login_page import LoginPage
from pages.main_page import MainPage


def test_login_successful(registration, logout):
        user, password = registration
        login_page = LoginPage()
        login_page.login(user, password)
        main_page = MainPage()
        main_page.assert_main_page_title('Niffler. The coin keeper.')


def test_invalid_login(registration):
        user, password = registration
        login_page = LoginPage()
        login_page.login(user, 'bad' + password)
        login_page.assert_bad_login('Bad credentials')