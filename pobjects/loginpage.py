from data.users import User
from pobjects.locators.loginlocators import LoginLocators


class LoginPage(LoginLocators):
    def navigate(self):
        self.page.goto('/')

    def do_login(self, user: User = None):
        user = user if user else self.user
        self.navigate()
        self.pobj.login.input_username.fill(user.login)
        self.pobj.login.input_password.fill(user.password)
        self.pobj.login.button_login.click()
        self.page.wait_for_url('/inventory.html')
