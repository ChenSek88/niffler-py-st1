import allure

from marks import TestData
from models.enums import Category
from pages.main_page import main_page
from pages.profile_page import profile_page


@allure.story("Profile")
def test_add_new_category(login_app_user, category_in_db, remove_all_categories, logout):
    main_page.go_to_profile()
    profile_page.add_category(Category.SCHOOL)
    main_page.assert_alert_message_and_close('New category added')
    profile_page.assert_added_category(Category.SCHOOL)
    assert category_in_db(Category.SCHOOL) == Category.SCHOOL


@TestData.category(Category.SCHOOL)
@allure.story("Profile")
def test_add_existing_category(category, login_app_user, logout):
    main_page.go_to_profile()
    profile_page.add_category(Category.SCHOOL)
    main_page.assert_alert_message_and_close('Can not add new category')


@allure.story("Profile")
def test_create_category_over_limits(login_app_user, add_max_count_categories, remove_all_categories, logout):
    main_page.go_to_profile()
    profile_page.add_category('OVER LIMITS')
    main_page.assert_alert_message_and_close('Can not add new category')


@allure.story("Profile")
def test_update_profile_settings(login_app_user, app_user, profile_data, firstname_surname_in_db, logout):
    username, _ = app_user
    name, surname = profile_data
    main_page.go_to_profile()
    profile_page.update_profile(name, surname)
    main_page.assert_alert_message_and_close('Profile successfully updated')
    profile_page.assert_changes(name, surname)
    assert firstname_surname_in_db(username) == (name, surname)
