from marks import TestData
from pages.main_page import main_page
from pages.profile_page import profile_page
import allure
from models.enums import Category


@allure.story("Profile")
def test_add_new_category(login_app_user, remove_all_categories, logout):
    main_page.go_to_profile()
    profile_page.add_category(Category.SCHOOL)
    main_page.assert_alert_message_and_close('New category added')
    profile_page.assert_added_category(Category.SCHOOL)


@TestData.category(Category.SCHOOL)
@allure.story("Profile")
def test_add_existing_category(category, login_app_user, logout):
    main_page.go_to_profile()
    profile_page.add_category(Category.SCHOOL)
    main_page.assert_alert_message_and_close('Can not add new category')
    profile_page.assert_added_category(Category.SCHOOL)


@allure.story("Profile")
def test_update_profile_settings(login_app_user, profile_data, logout):
    main_page.go_to_profile()
    name, surname = profile_data
    profile_page.update_profile(name, surname)
    main_page.assert_alert_message_and_close('Profile successfully updated')
    profile_page.assert_changes(name, surname)
