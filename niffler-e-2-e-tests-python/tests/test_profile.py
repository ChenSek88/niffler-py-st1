from pages.main_page import main_page
from pages.login_page import login_page
from pages.profile_page import profile_page


TEST_CATEGORY = 'QAGURU'


def test_add_new_category(registration, logout):
        username, password = registration
        login_page.login(username, password)
        main_page.go_to_profile()
        profile_page.add_category(TEST_CATEGORY)
        main_page.assert_alert_message_and_close('New category added')
        assert any(x.text == TEST_CATEGORY for x in profile_page.spending_categories())


def test_update_profile_settings(registration, update_profile_data, logout):
        username, password = registration
        login_page.login(username, password)
        main_page.go_to_profile()
        name, surname = update_profile_data
        profile_page.update_profile(name, surname)
        main_page.assert_alert_message_and_close('Profile successfully updated')
        profile_page.assert_changes(name, surname)

