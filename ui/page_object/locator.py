from collections import namedtuple

from selenium.webdriver.common.by import By

_Locator = namedtuple('Locator', ['by', 'value'])


def by_id(id_: str):
    return _Locator(By.ID, id_)


def by_xpath(xpath: str):
    return _Locator(By.XPATH, xpath)


def by_css(css: str):
    return _Locator(By.CSS_SELECTOR, css)
