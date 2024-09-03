from .base_page import BasePage
from selene import have


class PeoplePage(BasePage):

    def assert_empty_people_table(self, expected_text):
        self.assert_text('.people-content div', expected_text)


    def assert_people_in_table(self, username):
        people_table = self.find_element('.people-content tbody tr')
        elements = people_table.all('td')
        elements.should(have._texts_like(username))


    def add_friend(self):
        self.find_element('[data-tooltip-id=add-friend] button').click()


    def assert_message_in_table(self, expected_text):
        self.assert_text('.abstract-table__buttons div', expected_text)


    def accept_invitation(self):
        self.find_element('[data-tooltip-id=submit-invitation] button').click()


    def decline_invitation(self):
        self.find_element('[data-tooltip-id=decline-invitation] button').click()


    def add_friend_button_exists(self):
        self.find_element('[data-tooltip-id=add-friend] button')


people_page = PeoplePage()