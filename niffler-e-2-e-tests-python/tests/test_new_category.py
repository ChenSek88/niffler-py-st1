from pages.main_page import MainPage
from pages.profile_page import ProfilePage


CATEGORY = 'POP'

def test_add_new_category(login_test_user):
        login_test_user
        main_page = MainPage()
        main_page.go_to_profile()
        profile_page = ProfilePage()
        profile_page.add_category(CATEGORY)
        profile_page.assert_added_category(CATEGORY)