from playwright.sync_api import Page
from helpers.wrappers import LocatorDescriptor


class CommonLocators:
    cart_counter = LocatorDescriptor()
    'красный счетчик количества товаров в корзине'

    button_burger_menu = LocatorDescriptor()
    'меню "3 черты" слева-сверху'

    button_logout = LocatorDescriptor()
    'кнопка "Logout" сайдбара'

    button_close_cross = LocatorDescriptor()
    'кнопка "крестик" сайдбара'

    def __init__(self, page: Page) -> None:
        self.cart_counter = page.locator("//span[@class='shopping_cart_badge']")
        self.button_burger_menu = page.locator("//button[@id='react-burger-menu-btn']")
        self.button_logout = page.locator("//a[@id='logout_sidebar_link']")
        self.button_close_cross = page.locator("//button[@id='react-burger-cross-btn']")
