import os

import pytest
from _pytest.fixtures import SubRequest
from playwright.sync_api import Browser, BrowserContext
from playwright.sync_api import Page
from playwright.sync_api import Playwright

from pobjects.base import Base
from pobjects.allpages import PAGES

# from data.requests import envs
# from extra.thanks_for_order_page_check import ThanksForOrderPageCheck
from helpers.configs import ConfigurationsManager
# from page_object.cart_page import CartPage
# from page_object.catalogue_page import CataloguePage
# from page_object.checkout_page import CheckoutPage
# from page_object.favorite_page import FavoritePage
# from page_object.main_page import MainPage
# from page_object.orders_page import OrdersPage
# from page_object.page import Page
# from page_object.product_card_page import ProductCardPage
# from page_object.profile_page import ProfilePage
# from page_object.purchased_goods_page import PurchasedGoodsPage
# from page_object.search_results_page import SearchResultsPage
# from page_object.thanks_for_orders_page import ThanksForOrderPage
from helpers.video import VideoSettingsStrategy, AllureVideoSettings
# from support.wrapped_locators import wrapped_locator

config = ConfigurationsManager()
config.local_load_dotenv()


@pytest.fixture(scope='session')
def base_url():
    Base.base_url = os.getenv('BASE_URL', '').rstrip('/')
    return Base.base_url


@pytest.fixture
def video_settings(request):
    PW_VIDEO = os.getenv('PW_VIDEO')
    video = VideoSettingsStrategy().get(strategy=PW_VIDEO)
    yield video
    video.attach_to_allure(request)


@pytest.fixture
def browser(playwright: Playwright, request: SubRequest):
    is_headless = not request.config.getoption('--headed')
    browser = playwright.chromium.launch(headless=is_headless)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, video_settings: AllureVideoSettings, base_url: str):
    # video_attacher: AllureVideoAttacher
    context = browser.new_context(
        viewport={"width": 1600, "height": 900},
        record_video_dir=video_settings.record_video_dir,
        record_video_size=video_settings.record_video_size,
        base_url=base_url,
    )
    yield context
    context.close()


@pytest.fixture(scope='function')
def page(context: BrowserContext, video_settings: AllureVideoSettings):
    page = context.new_page()
    # page.set_default_timeout(20000)
    # page.set_default_navigation_timeout(45000)
    # page.locator = functools.partial(wrapped_locator, page)
    yield page
    video_settings.set_video_path_list(context)
    for page in context.pages:
        page.close()


@pytest.fixture(scope='function')
def pobj(page: Page):
    # video_attacher: AllureVideoAttacher,
    PAGES._lazy_init(page)
    Base.pobj = PAGES
    # page.set_default_timeout(20000)
    # page.set_default_navigation_timeout(45000)
    # page.locator = functools.partial(wrapped_locator, page)
    return PAGES
