import logging
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class document_state:
    def __init__(self, state: str = 'complete'):
        logger.debug(f'Explicitly wait till page state is equal to: {state}')
        self.state = state

    def __call__(self, driver: WebDriver):
        return driver.execute_script("return document.readyState;") == self.state
