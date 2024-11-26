import allure

from marks import TestData
from models.enums import Category
from pages.main_page import main_page
from pages.profile_page import profile_page


@allure.tag("WEB")
@allure.epic("Profile")
class TestProfilePage:
    def test_add_new_category(self, login_app_user, spend_db, remove_all_categories):
        main_page.go_to_profile()
        profile_page.add_category(Category.SCHOOL)
        main_page.assert_alert_message('New category added')
        profile_page.assert_added_category(Category.SCHOOL)
        assert spend_db.is_category_in_db(Category.SCHOOL)

    @TestData.category(Category.SCHOOL)
    def test_add_existing_category(self, category, login_app_user):
        main_page.go_to_profile()
        profile_page.add_category(Category.SCHOOL)
        main_page.assert_alert_message('Can not add new category')

    def test_create_category_over_limits(self, login_app_user, add_max_count_categories):
        main_page.go_to_profile()
        profile_page.add_category('OVER LIMITS')
        main_page.assert_alert_message('Can not add new category')

    def test_update_profile_settings(self, login_app_user, app_user, profile_data, userdata_db):
        username, _ = app_user
        name, surname = profile_data
        main_page.go_to_profile()
        profile_page.update_profile(name, surname)
        main_page.assert_alert_message('Profile successfully updated')
        profile_page.assert_changes(name, surname)
        assert userdata_db.firstname_surname_in_db(username)
