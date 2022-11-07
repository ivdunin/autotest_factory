from ui.page_object import PageElement
from ui.page_object import by_id
from ui.pages.bspb.bspb import BSPB


class OtpPage(BSPB):
    _page_path = '/auth/otp'
    otp_code = PageElement(by_id('otp-code'))
    btn_otp_login = PageElement(by_id('login-otp-button'))

    def enter_otp(self, otp: str):
        self.otp_code.send_keys(otp, clear=True)
        self.btn_otp_login.click()
