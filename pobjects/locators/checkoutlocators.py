from playwright.sync_api import Page

from pobjects.basepage import BasePage

from helpers.wrappers import LocatorDescriptor


class CheckOutLocators(BasePage):
    button_continue = LocatorDescriptor()
    'Кнопка "Продолжить"'

    button_cancel = LocatorDescriptor()
    'Кнопка "Cancel"'

    button_finish = LocatorDescriptor()
    'Кнопка "Finish"'

    button_back_home = LocatorDescriptor()
    'Кнопка "Back Home"'

    input_first_name = LocatorDescriptor()
    'Поле ввода "First Name"'

    input_second_name = LocatorDescriptor()
    'Поле ввода "Second Name"'

    input_zip_code = LocatorDescriptor()
    'Поле ввода "Postal code"'

    def __init__(self, page: Page):
        super().__init__(page)
        self.button_continue = page.locator("//input[@id='continue']")
        self.button_cancel = page.locator("//button[@data-test='cancel']")
        self.input_first_name = page.locator("//input[@data-test='firstName']")
        self.input_second_name = page.locator("//input[@data-test='lastName']")
        self.input_zip_code = page.locator("//input[@data-test='postalCode']")
        self.button_finish = page.locator("//button[@data-test='finish']")
        self.button_back_home = page.locator("//button[@data-test='back-to-products']")
