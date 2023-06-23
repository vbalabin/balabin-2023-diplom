import allure
from playwright.sync_api import Page

from data.literals import SuiteTitles as ST
from pobjects.allpages import AllPages
from helpers.wrappers import wrapped_expect as expect


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.MAIN)
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Главная. Добавить в корзину')
def test_add_to_cart(page: Page, pobj: AllPages):
    with allure.step('Предусловие: Аторизация, открыта Главная'):
        pobj.login.do_login()
        inventory_list = pobj.main.get_all_inventory_items()
    with allure.step('1 Кликнуть кнопку "Add to Cart" 1го товара'):
        inventory_list[0].add_to_cart.click()
        expect(pobj.main.common.cart_counter).to_have_text('1')
    with allure.step('2 Кликнуть кнопку "Add to Cart" 2го товара'):
        inventory_list[1].add_to_cart.click()
        expect(pobj.main.common.cart_counter).to_have_text('2')
    with allure.step('3 Кликнуть кнопку "Remove" 1го товара'):
        inventory_list[0].remove.click()
        expect(pobj.main.common.cart_counter).to_have_text('1')
    with allure.step('4 Кликнуть кнопку "Remove" 2го товара'):
        inventory_list[1].remove.click()
        expect(pobj.main.common.cart_counter).not_to_be_visible()
