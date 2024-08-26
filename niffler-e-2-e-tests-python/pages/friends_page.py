from .base_page import BasePage


class FriendsPage(BasePage):

    def assert_empty_friends_table(self, expected_text):
        self.assert_text('.people-content div', expected_text)


friends_page = FriendsPage()