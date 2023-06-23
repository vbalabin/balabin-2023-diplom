from copy import copy

import allure
from playwright.sync_api import Page

from data.literals import SuiteTitles as ST
from pobjects.allpages import AllPages


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.FILTERS)
@allure.severity(allure.severity_level.NORMAL)
@allure.title('Фильтры ZA')
def test_filters_za(page: Page, pobj: AllPages):
    with allure.step('Предусловие: Аторизация, открыта Главная'):
        pobj.login.do_login()
    with allure.step('1 выбрать сортировку ZA'):
        pobj.main.select_filter_option('za')
    with allure.step('2 получить список элементов'):
        inventory_list = pobj.main.get_all_inventory_items()
    with allure.step('3 порядок элементов совпадает с ожидаемым'):
        sorted_inventory_list = sorted(copy(inventory_list), key=lambda e: e.title, reverse=True)
        assert inventory_list == sorted_inventory_list, 'Проверка на порядок фильтрации НЕ ПРОШЛА'
