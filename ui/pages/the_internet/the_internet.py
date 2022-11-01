from config import cfg
from ui.page_object import BasePage, PageElement
from ui.page_object import by_css, by_id


class TheInternet(BasePage):
    _base_url = cfg.base_urls.the_internet


# FIXME: Don't do this! Use separate file for each class according to PEP8
# FIXME: This is just an example

class DropDown(TheInternet):
    _page_path = '/dropdown'
    select: PageElement = PageElement(by_css('select#dropdown'))


class DynamicControls(TheInternet):
    _page_path = '/dynamic_controls'
    checkbox: PageElement = PageElement(by_css('form#checkbox-example #checkbox'))
    button: PageElement = PageElement(by_css('form#checkbox-example button'))


class DynamicLoading(TheInternet):
    _page_path = '/dynamic_loading/'
    start: PageElement = PageElement(by_css('#start > button'))
    finish: PageElement = PageElement(by_id('finish'))
