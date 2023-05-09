import functools
import os
import re
import time
from datetime import datetime
from typing import List, Literal, Optional, Union, Pattern, overload

import allure
from playwright._impl._api_structures import Position
from playwright._impl._assertions import \
    APIResponseAssertions as APIResponseAssertionsImpl
from playwright._impl._assertions import \
    LocatorAssertions as LocatorAssertionsImpl
from playwright._impl._assertions import PageAssertions as PageAssertionsImpl
from playwright.sync_api._generated import (APIResponse, APIResponseAssertions,
                                            Locator, LocatorAssertions, Page,
                                            PageAssertions)


class WrappedLocator(Locator):

    @property
    def selector(self):
        res = re.search("selector='(.+)'", str(self))
        return res.group(1)

    def attach_screnshot(self, timeout: Optional[float], text: str = 'element'):
        if os.getenv('ATTACH_ELEMENTS'):
            _ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            allure.attach(
                self.screenshot(type='jpeg', timeout=timeout, quality=55),
                name=f"{text}-screenshot-{_ts}",
                attachment_type=allure.attachment_type.JPG)
        else:
            pass

    def click(self,
              *,
              modifiers: Optional[List[Literal['Alt', 'Control', 'Meta', 'Shift']]] = None,
              position: Optional[Position] = None,
              delay: Optional[float] = None,
              button: Optional[Literal['left', 'middle', 'right']] = None,
              click_count: Optional[int] = None,
              timeout: Optional[float] = None,
              force: Optional[bool] = None,
              no_wait_after: Optional[bool] = None,
              trial: Optional[bool] = None):
        with allure.step(f'click -> {self.selector}'):
            self.attach_screnshot(timeout=timeout)
        Locator.click(
            self, modifiers=modifiers, position=position, delay=delay, button=button,
            click_count=click_count, timeout=timeout, force=force,
            no_wait_after=no_wait_after, trial=trial
        )

    def fill(
            self,
            value: str,
            *,
            timeout: Optional[float] = None,
            no_wait_after: Optional[bool] = None,
            force: Optional[bool] = None):
        with allure.step(f'fill -> {self.selector}'):
            with allure.step(f'{value}'):
                pass
            self.attach_screnshot(timeout=timeout, text='before')
            Locator.fill(self, value, timeout=timeout, no_wait_after=no_wait_after, force=force)
            self.attach_screnshot(timeout=timeout, text='after')


def patch_locator(locator: Locator) -> WrappedLocator:
    # locator.click = functools.partial(WrappedLocator.click, locator)
    locator.__class__ = WrappedLocator
    return locator


class LocatorDescriptor:
    '''
    Оборачивает метод получения локатора из переменной класса,
    чтобы внедрить дополнительную логику
    '''

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, obj_type=None) -> WrappedLocator:
        locator: Locator = getattr(obj, self.private_name)
        # if os.getenv('IS_DEBUG_LOCATORS', 'true').upper() == 'TRUE':
        #     locator.highlight()
        #     locator.page.wait_for_timeout(2000)
        locator = patch_locator(locator)
        return locator

    def __set__(self, obj, value: Locator):
        setattr(obj, self.private_name, value)


@overload
def wrapped_expect(actual: Page, message: Optional[str] = None) -> PageAssertions:
    ...


@overload
def wrapped_expect(actual: Locator, message: Optional[str] = None) -> LocatorAssertions:
    ...


@overload
def wrapped_expect(actual: APIResponse, message: Optional[str] = None) -> APIResponseAssertions:
    ...


def wrapped_expect(
    actual: Union[Page, Locator, APIResponse], message: Optional[str] = None
) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
    if isinstance(actual, Page):
        return WrappedPageAssertions(PageAssertionsImpl(actual._impl_obj, message=message))
    elif isinstance(actual, Locator):
        res = WrappedLocatorAssertions(
            LocatorAssertionsImpl(actual._impl_obj, message=message)
        )
        res.actual = actual
        return res
    elif isinstance(actual, APIResponse):
        return APIResponseAssertions(
            APIResponseAssertionsImpl(actual._impl_obj, message=message)
        )
    raise ValueError(f"Unsupported type: {type(actual)}")


def add_to_positive_expect(func):
    @functools.wraps(func)
    def wrapper_method(self, *args, **kwargs):
        if isinstance(self.actual, WrappedLocator):
            with allure.step(f'expect -> {self.actual.selector} -> {func.__name__}'):
                try:
                    self.actual.attach_screnshot()
                except Exception:
                    pass
        func(self, *args, **kwargs)
    return wrapper_method


def add_to_negative_expect(func):
    @functools.wraps(func)
    def wrapper_method(self, *args, **kwargs):
        if isinstance(self.actual, WrappedLocator):
            with allure.step(f'expect -> {self.actual.selector} -> {func.__name__}'):
                pass
        func(self, *args, **kwargs)
    return wrapper_method


class WrappedLocatorAssertions(LocatorAssertions):
    actual: WrappedLocator = None

    @add_to_positive_expect
    def to_contain_text(self, *args, **kwargs) -> None:
        super().to_contain_text(*args, **kwargs)

    @add_to_positive_expect
    def not_to_contain_text(self, *args, **kwargs) -> None:
        super().not_to_contain_text(*args, **kwargs)

    @add_to_positive_expect
    def to_have_attribute(self, *args, **kwargs) -> None:
        super().to_have_attribute(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_attribute(self, *args, **kwargs) -> None:
        super().not_to_have_attribute(*args, **kwargs)

    @add_to_positive_expect
    def to_have_class(self, *args, **kwargs) -> None:
        super().to_have_class(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_class(self, *args, **kwargs) -> None:
        super().not_to_have_class(*args, **kwargs)

    @add_to_positive_expect
    def to_have_count(self, *args, **kwargs) -> None:
        super().to_have_count(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_count(self, *args, **kwargs) -> None:
        super().not_to_have_count(*args, **kwargs)

    @add_to_positive_expect
    def to_have_css(self, *args, **kwargs) -> None:
        super().to_have_css(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_css(self, *args, **kwargs) -> None:
        super().not_to_have_css(*args, **kwargs)

    @add_to_positive_expect
    def to_have_id(self, *args, **kwargs) -> None:
        super().to_have_id(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_id(self, *args, **kwargs) -> None:
        super().not_to_have_id(*args, **kwargs)

    @add_to_positive_expect
    def to_have_js_property(self, *args, **kwargs) -> None:
        super().to_have_js_property(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_js_property(self, *args, **kwargs) -> None:
        super().not_to_have_js_property(*args, **kwargs)

    @add_to_positive_expect
    def to_have_value(self, *args, **kwargs) -> None:
        super().to_have_value(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_value(self, *args, **kwargs) -> None:
        super().not_to_have_value(*args, **kwargs)

    @add_to_positive_expect
    def to_have_values(self, *args, **kwargs) -> None:
        super().to_have_values(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_values(self, *args, **kwargs) -> None:
        super().not_to_have_values(*args, **kwargs)

    @add_to_positive_expect
    def to_have_text(self, *args, **kwargs) -> None:
        super().to_have_text(*args, **kwargs)

    @add_to_positive_expect
    def not_to_have_text(self, *args, **kwargs) -> None:
        super().not_to_have_text(*args, **kwargs)

    @add_to_positive_expect
    def to_be_checked(self, *args, **kwargs) -> None:
        super().to_be_checked(*args, **kwargs)

    @add_to_positive_expect
    def not_to_be_checked(self, *args, **kwargs) -> None:
        super().not_to_be_checked(*args, **kwargs)

    @add_to_positive_expect
    def to_be_disabled(self, *args, **kwargs) -> None:
        super().to_be_disabled(*args, **kwargs)

    @add_to_positive_expect
    def not_to_be_disabled(self, *args, **kwargs) -> None:
        super().not_to_be_disabled(*args, **kwargs)

    @add_to_positive_expect
    def to_be_editable(self, *args, **kwargs) -> None:
        super().to_be_editable(*args, **kwargs)

    @add_to_positive_expect
    def not_to_be_editable(self, *args, **kwargs) -> None:
        super().not_to_be_editable(*args, **kwargs)

    @add_to_positive_expect
    def to_be_empty(self, *args, **kwargs) -> None:
        super().to_be_empty(*args, **kwargs)

    @add_to_positive_expect
    def not_to_be_empty(self, *args, **kwargs) -> None:
        super().not_to_be_empty(*args, **kwargs)

    @add_to_positive_expect
    def to_be_enabled(self, *args, **kwargs) -> None:
        super().to_be_enabled(*args, **kwargs)

    @add_to_positive_expect
    def not_to_be_enabled(self, *args, **kwargs) -> None:
        super().not_to_be_enabled(*args, **kwargs)

    @add_to_negative_expect
    def to_be_hidden(self, *args, **kwargs) -> None:
        super().to_be_hidden(*args, **kwargs)

    @add_to_positive_expect
    def not_to_be_hidden(self, *args, **kwargs) -> None:
        super().not_to_be_hidden(*args, **kwargs)

    @add_to_positive_expect
    def to_be_visible(self, *args, **kwargs) -> None:
        super().to_be_visible(*args, **kwargs)

    @add_to_negative_expect
    def not_to_be_visible(self, *args, **kwargs) -> None:
        super().not_to_be_visible(*args, **kwargs)

    @add_to_positive_expect
    def to_be_focused(self, *args, **kwargs) -> None:
        super().to_be_focused(*args, **kwargs)

    @add_to_positive_expect
    def not_to_be_focused(self, *args, **kwargs) -> None:
        super().not_to_be_focused(*args, **kwargs)


class WrappedPageAssertions(PageAssertions):
    def to_have_title(
        self,
        title_or_reg_exp: Union[Pattern[str], str],
        *,
        timeout: Optional[float] = None
    ) -> None:
        with allure.step('expect -> page -> to_have_title'):
            with allure.step(f'title_or_reg_exp: "{title_or_reg_exp}"'):
                super().to_have_title(title_or_reg_exp, timeout=timeout)

    def not_to_have_title(
        self,
        title_or_reg_exp: Union[Pattern[str], str],
        *,
        timeout: Optional[float] = None
    ) -> None:
        with allure.step('expect -> page -> not_to_have_title'):
            with allure.step(f'title_or_reg_exp: "{title_or_reg_exp}"'):
                super().not_to_have_title(title_or_reg_exp, timeout=timeout)

    def to_have_url(
        self,
        url_or_reg_exp: Union[str, Pattern[str]],
        *,
        timeout: Optional[float] = None
    ) -> None:
        with allure.step('expect -> page -> to_have_url'):
            with allure.step(f'url_or_reg_exp: "{url_or_reg_exp}"'):
                super().to_have_url(url_or_reg_exp, timeout=timeout)

    def not_to_have_url(
        self,
        url_or_reg_exp: Union[Pattern[str], str],
        *,
        timeout: Optional[float] = None
    ) -> None:
        with allure.step('expect -> page-> not_to_have_url'):
            with allure.step(f'url_or_reg_exp: "{url_or_reg_exp}"'):
                super().not_to_have_url(url_or_reg_exp, timeout=timeout)
