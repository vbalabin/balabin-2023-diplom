from playwright.sync_api import Page

from pobjects.basepage import BasePage

from helpers.wrappers import LocatorDescriptor


class CartLocators(BasePage):
    button_continue_shopping = LocatorDescriptor()
    'кнопка "Continue shopping" слева страницы'

    button_checkout = LocatorDescriptor()
    'кнопка "Checkout" справа'

    cart_item = LocatorDescriptor()
    'товар в корзине'

    def __init__(self, page: Page):
        super().__init__(page)
        self.button_continue_shopping = page.locator("//button[@id='continue-shopping']")
        self.button_checkout = page.locator("//button[@data-test='checkout']")
        self.cart_item = page.locator("//div[@class='cart_item']")
