from abc import ABC

from selenium.common import TimeoutException
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from config import DEFAULT_TIMEOUT
from ui.page_object.abstract_element import AbstractElement
from ui.page_object.locator import _Locator


class Element(AbstractElement, ABC):
    def __init__(self, locator: _Locator, web_element: WebElement = None):
        super().__init__(locator)
        self._web_element: WebElement = web_element

    @property
    def web_element(self) -> WebElement:
        """ Property to access raw Selenium WebElement """
        return self._web_element

    @property
    def shadow_root(self) -> ShadowRoot:
        """ Property to get ShadowRoot element """
        return self._web_element.shadow_root

    @classmethod
    def create(cls, driver: WebDriver, locator: _Locator, element: WebElement):
        """ Create and instance of element with given locator """
        assert isinstance(element, WebElement), f'Cannot init PageElement with {type(element)}'

        el = cls(locator, element)
        el.initiate(driver, find=False)
        return el

    def is_visible(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """ Check that found element is visible """
        try:
            WebDriverWait(self._driver, timeout=timeout).until(
                EC.visibility_of(self._web_element),
                message=f'Element ({self}) not visible on page: {self._driver.current_url}!'
            )
            return True
        except TimeoutException as e:
            self._logger.warning(e)
            return False

    def click(self):
        """ Click on found element """
        if self.is_visible():
            self._web_element.click()
        else:
            raise AssertionError('Cannot click on invisible element!')

    def attribute(self, attr_name: str) -> str:
        """ Get element attribute """
        attribute = self._web_element.get_attribute(attr_name)
        return attribute

    @property
    def is_selected(self) -> bool:
        """ Get checkbox state """
        return self._web_element.is_selected()

    @property
    def text(self) -> str:
        """ Get element text attribute """
        text = self._web_element.text
        return text

    def select_by_value(self, value: str):
        """ Select dropdown element by value """
        select = Select(self._web_element)
        select.select_by_value(value)

    def select_by_visible_text(self, text: str):
        """ Select dropdown element by visible text """
        select = Select(self._web_element)
        select.select_by_visible_text(text)
