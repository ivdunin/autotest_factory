import logging
import random

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config import cfg

pytest_plugins = ("hooks",)
logger = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    """ Faker fixture

    * https://faker.readthedocs.io/en/master/index.html and
    * https://faker.readthedocs.io/en/master/pytest-fixtures.html """
    return [cfg.faker.locale]


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return random.randint(1, 10)


@pytest.fixture
def browser(request) -> WebDriver:
    """ Browser fixture

    Manage WebDriver object
    * Init it with a desired options.
    * Attach screenshots on errors
    * Quit browser on test finish
    """
    chrome_options = ChromeOptions()
    if request.config.getoption('headless', False):
        chrome_options.add_argument('--headless')

    chrome_options.add_argument('window-size={0}'.format(cfg.webdriver.browser.window_size))
    browser = webdriver.Chrome(options=chrome_options)

    yield browser

    try:
        if request.node.rep_setup.failed or request.node.rep_call.failed:
            logger.error(f"Failed on page: '{browser.current_url}'")
            allure.attach(browser.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG,
                          name=request.node.nodeid)
    except AttributeError as e:
        logger.warning(f"Cannot capture screenshot! {e}")

    browser.quit()
