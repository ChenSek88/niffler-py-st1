from selene.support.jquery_style_selectors import s
from selene import browser

class BasePage:
    def open_url(self, url):
        browser.open_url(url)


    def find_element(self, selector):
        return s(selector)


    def assert_text(self, selector, expected_text):
        actual_text = self.find_element(selector).text
        assert actual_text == expected_text
