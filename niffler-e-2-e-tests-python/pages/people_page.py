from .base_page import BasePage
from selene import have


class PeoplePage(BasePage):

    def assert_empty_people_table(self, expected_text):
        self.assert_text('.people-content div', expected_text)


    def assert_friend_in_table(self, friend):
        people_table = self.find_element('.people-content tbody tr')
        elements = people_table.all('td')
        elements.should(have._texts_like(friend))


    def add_friend(self):
        self.find_element('[data-tooltip-id=add-friend] button').click()


    def assert_pending_invitation(self):
        self.find_element('.abstract-table__buttons div').should(have.value('Pending invitation'))


people_page = PeoplePage()