from .base_page import BasePage


class ProfilePage(BasePage):
    def assert_category_title(self, expected_text):
        self.find_element('.main-content__section-add-category h2')


    def add_category(self, category):
        self.find_element('input[name=category]').set_value(category)
        self.find_element('.add-category__input-container button').click()


    def assert_added_category(self, expected_category):
        self.assert_text('.categories__list', expected_category)