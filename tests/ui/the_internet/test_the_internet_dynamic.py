import allure

from ui.pages.the_internet.the_internet import DynamicLoading

pytestmark = allure.suite("The internet test suite")


def test_dynamic_loading_1(browser):
    """ Dynamic loading test """
    dl = DynamicLoading(browser).open(wait_page_loaded=True, additional_path='1')
    dl.start.click_and_disappear()

    dl.finish.wait_to_be_visible()
    assert dl.finish.text == 'Hello World!'


def test_dynamic_loading_2(browser):
    """ Dynamic loading test """
    dl = DynamicLoading(browser).open(wait_page_loaded=True, additional_path='2')
    dl.start.click_and_disappear()

    dl.finish.wait_to_be_visible()
    assert dl.finish.text == 'Hello World!'
