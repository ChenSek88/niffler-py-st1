from .base_page import BasePage



class PeoplePage(BasePage):

    def assert_empty_people_table(self, expected_text):
        self.assert_text('.people-content div', expected_text)


people_page = PeoplePage()