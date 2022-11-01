import allure

from ui.pages.the_internet.the_internet import DropDown, DynamicControls

pytestmark = allure.suite("The internet test suite")


@allure.description_html("<b>Test drop down</b>")
def test_dropdown(browser):
    dropdown = DropDown(browser)
    dropdown.open()

    dropdown.select.select_by_value('1')
    dropdown.get_screenshot('opt 1')
    dropdown.select.select_by_visible_text('Option 2')
    dropdown.get_screenshot('opt 2')


@allure.description('Dynamic controls test')
def test_dynamic_controls(browser):
    dc = DynamicControls(browser).open()
    dc.button.click()
    dc.checkbox.wait_to_disappear()

    dc.button.click()
    dc.checkbox.wait_to_be_visible()
    dc.checkbox.click()

    dc.get_screenshot('dynamic_control')
