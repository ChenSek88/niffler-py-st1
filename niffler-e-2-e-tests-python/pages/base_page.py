from selene.support.shared.jquery_style import s
from selene import browser, have


class BasePage:

    def open_url(self, url):
        browser.driver.maximize_window()
        browser.open(url)

    def find_element(self, selector):
        return s(selector)

    def assert_text(self, selector, expected_text):
        self.find_element(selector).should(have.text(expected_text))
