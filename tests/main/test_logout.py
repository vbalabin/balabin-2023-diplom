import allure
import pytest
from playwright.sync_api import Page
from data.users import standard_user, performance_glitch_user

from data.literals import SuiteTitles as ST
from helpers.wrappers import wrapped_expect as expect
from pobjects.allpages import AllPages


@allure.parent_suite(ST.SAUCEDEMO)
@allure.suite(ST.MAIN)
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Главная. Разлогин')
@pytest.mark.parametrize('user', [standard_user, performance_glitch_user],
                         ids=['standard_user', 'performance_glitch_user'],
                         indirect=True)
def test_logout(page: Page, pobj: AllPages):
    with allure.step('Предусловие: Аторизация, открыта Главная'):
        pobj.login.do_login()
    with allure.step('1 Открыть сайдбар'):
        pobj.main.common.button_burger_menu.click()
    with allure.step('2 Нажать крестик'):
        pobj.main.common.button_close_cross.click()
    with allure.step('3 Открыть сайдбар'):
        pobj.main.common.button_burger_menu.click()
    with allure.step('4 Нажать "Logout"'):
        pobj.main.common.button_logout.click()
    with allure.step('Проверка: открыта страница Авторизация'):
        expect(page).to_have_url('/')
