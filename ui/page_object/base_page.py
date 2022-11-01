""" https://selenium-python.readthedocs.io/page-objects.html """

import logging
from urllib.parse import urljoin

import allure
from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from config import PAGE_LOAD_TIMEOUT
from ui.page_object.expected_condition.document_state import document_state
from ui.page_object.page_element import PageElement
from ui.page_object.page_elements import PageElements


class BasePage:
    """ Base class for all page objects """
    _base_url = None
    _page_path = None
    _logger = logging.getLogger(__name__)

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def __repr__(self):
        return '{cls}(url={url})'.format(cls=self.__class__.__name__, url=urljoin(self._base_url, self._page_path))

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def current_url(self) -> str:
        """ Get page url """
        return self._driver.current_url

    def get_screenshot(self, name: str):
        """ Create page screenshot """
        allure.attach(self._driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG, name=name)

    def open(self, wait_page_loaded: bool = False, additional_path: str = ''):
        """ Open page assigned to a Page Class """
        assert self._base_url, ' variable _base_url cannot be empty!'
        if self._page_path:
            url = urljoin(self._base_url, self._page_path)
        else:
            url = self._base_url

        if additional_path:
            url = urljoin(url, additional_path)

        self._logger.info(f'Open url: {url}')
        self._driver.get(url)
        if wait_page_loaded:
            assert self.wait_page_loaded(), 'Page not loaded!'

        return self

    def wait_page_loaded(self, timeout: int = PAGE_LOAD_TIMEOUT) -> bool:
        """ Wait till page loaded (document.readyState == complete) """
        try:
            WebDriverWait(self._driver, timeout).until(document_state())
            return True
        except TimeoutException:
            self._logger.warning(f'Page <{self.current_url}> not loaded before timeout!')
            return False

    def scroll_down(self):
        """ Scroll down to the page bottom """
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_up(self):
        """ Scroll up to the page top """
        self._driver.execute_script("window.scrollTo(0, 0);")

    def __enter__(self):
        self._logger.debug(f'Init page object for: {self.__class__.__name__}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._logger.debug(f'Destroy page object for: {self.__class__.__name__}')
        self._driver = None

    def __getattribute__(self, item):
        """ Initiate WebDriver for each element when accessing it.

        The main idea here is: when we try to access any attribute of a Page class and this attribute PageElement or
        PageElements we should init driver
        """
        attr = object.__getattribute__(self, item)

        if isinstance(attr, (PageElement, PageElements)):
            attr.initiate(drv=self._driver)

        return attr
