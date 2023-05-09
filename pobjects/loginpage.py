from pobjects.locators.loginlocators import LoginLocators
from data.users import User


class LoginPage(LoginLocators):
    def navigate(self):
        self.page.goto('/')

    def do_login(self, user: User):
        return
