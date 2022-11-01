from ui.page_object import PageElement
from ui.page_object import by_css
from ui.pages.bspb.bspb import BSPB


class StatementPage(BSPB):
    _page_path = '/statement'
    header: PageElement = PageElement(by_css('#contentbar h1'))

    def get_header(self):
        return self.header.text
