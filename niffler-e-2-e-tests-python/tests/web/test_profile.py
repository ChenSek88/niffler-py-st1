import allure

from marks import TestData
from models.enums import Category
from pages.main_page import main_page
from pages.profile_page import profile_page


@allure.epic("WEB")
@allure.story("Profile")
def test_add_new_category(login_app_user, is_category_in_db, remove_all_categories):
    main_page.go_to_profile()
    profile_page.add_category(Category.SCHOOL)
    main_page.assert_alert_message('New category added')
    profile_page.assert_added_category(Category.SCHOOL)
    assert is_category_in_db(Category.SCHOOL) == Category.SCHOOL


@allure.epic("WEB")
@allure.story("Profile")
@TestData.category(Category.SCHOOL)
def test_add_existing_category(category, login_app_user):
    main_page.go_to_profile()
    profile_page.add_category(Category.SCHOOL)
    main_page.assert_alert_message('Can not add new category')


@allure.epic("WEB")
@allure.story("Profile")
def test_create_category_over_limits(login_app_user, add_max_count_categories, remove_all_categories):
    main_page.go_to_profile()
    profile_page.add_category('OVER LIMITS')
    main_page.assert_alert_message('Can not add new category')


@allure.epic("WEB")
@allure.story("Profile")
def test_update_profile_settings(login_app_user, app_user, profile_data, is_firstname_surname_in_db):
    username, _ = app_user
    name, surname = profile_data
    main_page.go_to_profile()
    profile_page.update_profile(name, surname)
    main_page.assert_alert_message('Profile successfully updated')
    profile_page.assert_changes(name, surname)
    assert is_firstname_surname_in_db(username) == (name, surname)
