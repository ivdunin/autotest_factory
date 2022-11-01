from ui.page_object import PageElement
from ui.page_object import by_css
from ui.pages.bspb.bspb import BSPB


class PhonePaymentPage(BSPB):
    _page_path = '/vendors/unified-phone-payment'

    phone_number: PageElement = PageElement(by_css('input[name="phoneNumber"]'))
    payment_amount: PageElement = PageElement(by_css('input[name="payment.amount"]'))
    payment_comment: PageElement = PageElement(by_css('input[name="payment.comment"]'))
    btn_pay: PageElement = PageElement(by_css('button#forward'))
    btn_draft: PageElement = PageElement(by_css('button[data-save-mode="SAVE_AS_DRAFT"]'))

    def phone_payment(self, phone_number: str, amount: int, draft: bool = False, comment: str = ''):
        self.phone_number.send_keys(phone_number, clear=True)
        self.payment_amount.send_keys(str(amount), clear=True)

        if comment:
            self.payment_comment.send_keys(comment)

        if draft:
            self.btn_draft.click_and_disappear()
        else:
            self.btn_pay.click_and_disappear()
