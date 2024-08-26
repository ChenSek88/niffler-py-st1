from pages.main_page import main_page
from pages.profile_page import profile_page


TEST_CATEGORY = 'EDUCATION'


def test_add_new_category(login_app_user, logout):
        main_page.go_to_profile()
        profile_page.add_category(TEST_CATEGORY)
        main_page.assert_alert_message_and_close('New category added')
        profile_page.assert_added_category(TEST_CATEGORY)


def test_update_profile_settings(login_app_user, profile_data, logout):
        main_page.go_to_profile()
        name, surname = profile_data
        profile_page.update_profile(name, surname)
        main_page.assert_alert_message_and_close('Profile successfully updated')
        profile_page.assert_changes(name, surname)

