from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import DEFAULT_TIMEOUT
from ui.page_object.element import Element
from ui.page_object.locator import _Locator


class PageElement(Element):
    def __init__(self, locator: _Locator, skip_initial_search: bool = False):
        super().__init__(locator)
        self._skip_initial_search = skip_initial_search

    def find(self, timeout: int = DEFAULT_TIMEOUT):
        """ Find element on the page, store result in self._web_element

        :param timeout: wait for element to be present in DOM
        :raise AssertionError: if element not present in DOM
        """
        if self._skip_initial_search:
            self._logger.warning(f'Skip for initial search: {self}')
            self._skip_initial_search = False
            return

        self._logger.debug(f'Search for: {self}')
        try:
            self._web_element = WebDriverWait(self._driver, timeout=timeout).until(
                EC.presence_of_element_located(self._locator),
                message=f'Element with locator: {self._locator} not found on page: {self._driver.current_url}!'
            )
        except TimeoutException as e:
            raise AssertionError(e)

    def send_keys(self, txt: str, clear: bool = False, timeout: int = DEFAULT_TIMEOUT):
        """ Input text into an element """
        self._logger.debug(f'Input text: "{txt}" into: {self}')
        self._web_element = self._is_interactable(timeout)

        if clear:
            self._web_element.clear()
        self._web_element.send_keys(txt)

    def _is_interactable(self, timeout: int) -> WebElement:
        """ Check element is interactable (for send_keys, click) """
        try:
            element = WebDriverWait(self._driver, timeout=timeout).until(
                EC.element_to_be_clickable(self._locator),
                message=f'Element {self._locator} not interactable on a page: {self._driver.current_url}!'
            )
            return element
        except TimeoutException as e:
            raise AssertionError(e)

    def wait_to_be_visible(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """ Element should be present and visible ob a page! """
        self._logger.debug(f'Check presence: {self}')
        try:
            WebDriverWait(self._driver, timeout=timeout).until(
                EC.visibility_of_element_located(self._locator),
                message=f'Element {self._locator} not visible on a page: {self._driver.current_url}!'
            )
            return True
        except TimeoutException as e:
            self._logger.warning(e)
            return False

    def wait_to_disappear(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """ Wait for element disappear (not visible) """
        self._logger.debug(f'Check absence: {self}')
        try:
            WebDriverWait(self._driver, timeout=timeout).until(
                EC.invisibility_of_element(self._locator),
                message=f'Element {self._locator} still visible on a page: {self._driver.current_url}!'
            )
            return True
        except TimeoutException as e:
            self._logger.warning(e)
            return False

    def click(self, timeout: int = DEFAULT_TIMEOUT):
        """ Check if element clickable and click """
        self._logger.debug(f'Click on: {self}')
        try:
            self._web_element = self._is_interactable(timeout)
            self._web_element.click()
        except ElementClickInterceptedException as e:
            raise AssertionError(e)

    def click_and_disappear(self, timeout: int = DEFAULT_TIMEOUT):
        """ Check if element disappear after click """
        self.click(timeout)
        assert self.wait_to_disappear(timeout=timeout), f'Element {self._locator} still visible after click!'

    def mouse_over(self, timeout: int = DEFAULT_TIMEOUT, click: bool = False):
        """ Move mouse to element, element should be visible on screen """
        self._logger.debug(f'Move mouse to: {self}')
        self.find(timeout=timeout)
        action = ActionChains(self._driver)
        action.move_to_element(self._web_element)
        if click:
            action.click()
        action.perform()
