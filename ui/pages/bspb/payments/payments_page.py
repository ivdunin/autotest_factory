from ui.page_object import PageElement
from ui.page_object import by_css
from ui.pages.bspb.bspb import BSPB


class PaymentsPage(BSPB):
    _page_path = '/payments/dashboard'
    self_phone = PageElement(by_css('div#dashboard-favorites div[title="Мой телефон"]'))

    def do_phone_payment(self):
        self.self_phone.click_and_disappear()
