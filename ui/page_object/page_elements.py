from typing import List

from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import DEFAULT_TIMEOUT
from ui.page_object.abstract_element import AbstractElement
from ui.page_object.element import Element
from ui.page_object.locator import _Locator


class PageElements(AbstractElement):
    def __init__(self, locator: _Locator):
        super().__init__(locator)
        self._index = 0
        self._web_elements: List[WebElement] = []

    @property
    def elements(self) -> List[WebElement]:
        return self._web_elements

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self) -> Element:
        if self._index >= len(self._web_elements):
            raise StopIteration
        else:
            element = self._web_elements[self._index]
            self._index += 1

            return Element.create(self._driver, self._locator, element)

    def find(self, timeout: int = DEFAULT_TIMEOUT):
        """ Find any elements on the page """
        try:
            self._logger.debug(f'Find elements: {self._locator}')
            self._web_elements = WebDriverWait(self._driver, timeout=timeout).until(
                EC.presence_of_all_elements_located(self._locator),
                message=f'Element with locator: {self._locator} not found on page!'
            )
        except TimeoutException as e:
            raise AssertionError(e)

    def count(self, update: bool = False) -> int:
        """ Count elements on page """
        if update:
            self.find()

        return len(self._web_elements)

