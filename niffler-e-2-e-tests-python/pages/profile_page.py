from .base_page import BasePage
from selene import browser

class ProfilePage(BasePage):
    def assert_category_title(self, expected_text):
        self.find_element('.main-content__section-add-category h2')


    def add_category(self, category):
        self.find_element('input[name=category]').set_value(category)
        self.find_element('.add-category__input-container button').click()


    def spending_categories(self):
        categories_list = self.find_element('.categories__list')
        return categories_list.elements('.categories__item')

    def update_profile(self, name, surname):
        self.find_element('input[name=firstname]').set_value(name)
        self.find_element('input[name=surname]').set_value(surname)
        self.find_element('[type=submit]').click()


    def assert_changes(self, name, surname):
        name_value = self.find_element('input[name=firstname]').get_attribute('value')
        surname_value = self.find_element('input[name=surname]').get_attribute('value')
        assert name_value == name
        assert surname_value == surname