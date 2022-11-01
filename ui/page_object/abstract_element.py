import logging
from abc import abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from config import DEFAULT_TIMEOUT
from ui.page_object.locator import _Locator


class AbstractElement:
    _logger = logging.getLogger(__name__)

    def __init__(self, locator: _Locator):
        assert isinstance(locator, _Locator), f'locator expected to be: {type(_Locator)}; got {type(locator)}'

        self._locator = locator
        self._driver = None

    @abstractmethod
    def find(self, timeout: int = DEFAULT_TIMEOUT):
        pass

    def initiate(self, drv: WebDriver, find: bool = True):
        """ Init PageElement with WebDriver instance and search for element(s) """
        assert isinstance(drv, WebDriver), f'Cannot init with {type(drv)}'

        self._driver = drv
        if find:
            self.find()

        return self

    def __repr__(self):
        return '{cls}({loc})'.format(cls=self.__class__.__name__, loc=self._locator)
