import allure
from playwright.sync_api import Page

from data.literals import SuiteTitles as ST
from pobjects.allpages import AllPages
from helpers.wrappers import wrapped_expect as expect


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.CART)
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Корзина. Клик по кнопке "Continue shopping"')
def test_cart_items(page: Page, pobj: AllPages):
    items_number = 3
    with allure.step('Предусловие: Авторизация, открыта Главная'):
        pobj.login.do_login()
    with allure.step(f'1 Добавить {items_number} товаров в корзину'):
        pobj.main.add_items_to_cart(items_number)
    with allure.step('2 Перейти в корзину'):
        pobj.main.button_cart.click()
        pobj.cart.cart_item.wait_dom_loaded(timeout=500)
    with allure.step('Проверка: в корзине есть выбранные товары'):
        items = pobj.cart.get_all_inventory_items()
        assert len(items) == items_number
    with allure.step('3 Клик по кнопке "Continue shopping"'):
        pobj.cart.button_continue_shopping.click()
        expect(page).to_have_url('/inventory.html')
