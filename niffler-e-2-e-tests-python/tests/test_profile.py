from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


TEST_CATEGORY = 'QAGURU'


def test_add_new_category(registration):
        username, password = registration
        login_page = LoginPage()
        login_page.login(username, password)
        main_page = MainPage()
        main_page.go_to_profile()
        profile_page = ProfilePage()
        profile_page.add_category(TEST_CATEGORY)
        assert any(x.text == TEST_CATEGORY for x in profile_page.spending_categories())


def test_update_profile_settings(registration, update_profile_data):
        username, password = registration
        login_page = LoginPage()
        login_page.login(username, password)
        main_page = MainPage()
        main_page.go_to_profile()
        profile_page = ProfilePage()
        name, surname = update_profile_data
        profile_page.update_profile(name, surname)
        profile_page.assert_changes(name, surname)
