import os

import pytest
from _pytest.fixtures import SubRequest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from data.users import User, standard_user
from helpers.configs import ConfigurationsManager
from helpers.video import AllureVideoSettings, VideoSettingsStrategy
from pobjects.allpages import PAGES
from pobjects.basepage import BasePage

config = ConfigurationsManager()
config.local_load_dotenv()


@pytest.fixture(scope='session')
def base_url():
    BasePage.base_url = os.getenv('BASE_URL', '').rstrip('/')
    return BasePage.base_url


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
    context = browser.new_context(
        viewport={"width": 1600, "height": 900},
        record_video_dir=video_settings.record_video_dir,
        record_video_size=video_settings.record_video_size,
        base_url=base_url,
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext, video_settings: AllureVideoSettings):
    page = context.new_page()
    page.set_default_timeout(20000)
    page.set_default_navigation_timeout(20000)
    yield page
    video_settings.set_video_path_list(context)
    for page in context.pages:
        page.close()


@pytest.fixture
def user(request: SubRequest):
    requested_user = getattr(request, 'param', standard_user)
    return requested_user


@pytest.fixture
def pobj(page: Page, user: User):
    PAGES._lazy_init(page)
    BasePage.pobj = PAGES
    BasePage.user = user
    return PAGES
