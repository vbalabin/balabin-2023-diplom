import allure
from playwright.sync_api import Page

from data.literals import SuiteTitles as ST
from pobjects.allpages import AllPages
from helpers.wrappers import wrapped_expect as expect


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.CART)
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Корзина. Удалить из корзины')
def test_remove_from_cart(page: Page, pobj: AllPages):
    items_number = 3
    with allure.step('Предусловие: Авторизация, добавлены товары в корзину, открыта корзина'):
        pobj.login.do_login()
        pobj.main.add_items_to_cart(items_number)
        pobj.main.button_cart.click()
        pobj.cart.cart_item.wait_dom_loaded(timeout=500)
    with allure.step('1 Очистить корзину'):
        pobj.cart.clear_cart()
    with allure.step('Проверка: в корзине нет товаров'):
        expect(pobj.main.common.cart_counter).not_to_be_visible()
    with allure.step('2 Клик по кнопке "Continue shopping"'):
        pobj.cart.button_continue_shopping.click()
