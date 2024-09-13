from pages.main_page import main_page
from pages.profile_page import profile_page
from marks import Pages
import allure


TEST_CATEGORY = 'EDUCATION'


@Pages.spending_page
@allure.story("Profile")
def test_add_new_category(remove_all_categories, logout):
        main_page.go_to_profile()
        profile_page.add_category(TEST_CATEGORY)
        main_page.assert_alert_message_and_close('New category added')
        profile_page.assert_added_category(TEST_CATEGORY)


@Pages.spending_page
@allure.story("Profile")
def test_update_profile_settings(profile_data, logout):
        main_page.go_to_profile()
        name, surname = profile_data
        profile_page.update_profile(name, surname)
        main_page.assert_alert_message_and_close('Profile successfully updated')
        profile_page.assert_changes(name, surname)
