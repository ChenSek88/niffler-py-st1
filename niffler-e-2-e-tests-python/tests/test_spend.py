from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.main_page import MainPage


CATEGORY = 'QAGURU'


def test_add_spending(registration):
        username, password = registration
        login_page = LoginPage()
        login_page.login(username, password)
        main_page = MainPage()
        main_page.go_to_profile()
        profile_page = ProfilePage()
        profile_page.add_category(CATEGORY)
        assert any(x.text == CATEGORY for x in profile_page.spending_categories())