from ui.page_object import PageElement
from ui.page_object import by_id
from ui.pages.bspb.bspb import BSPB
from ui.pages.bspb.main_menu import MainMenu


class WelcomePage(BSPB, MainMenu):
    _page_path = '/welcome'
    btn: PageElement = PageElement(by_id('HINT_Bank-overview-full'), skip_initial_search=True)

    def close_popup(self):
        try:
            self.btn.click(timeout=2)
        except AssertionError:
            pass
