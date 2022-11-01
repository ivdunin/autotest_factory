from typing import List

from ui.page_object import PageElement, PageElements
from ui.page_object import by_css, by_id
from ui.pages.bspb.bspb import BSPB


class PaymentsHistory(BSPB):
    _page_path = '/payments/history'
    btn_apply_filter: PageElement = PageElement(by_id('apply-payments-filter'))
    payment_history: PageElements = PageElements(by_css('table#payment-history tr'))

    def get_payment_history(self) -> List[str]:
        history = []
        for ph in self.payment_history:
            ph.find()
            history.append(ph.text)

        return history


