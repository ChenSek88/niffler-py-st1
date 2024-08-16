from .base_page import BasePage


class MainPage(BasePage):
    header_title = 'Niffler. The coin keeper.'
    logout = '.header__logout button'

    def assert_main_page_title(self, expected_text):
        self.assert_text('.header__title', expected_text)


    def go_to_profile(self):
        self.find_element('a[href*=profile]').click()
