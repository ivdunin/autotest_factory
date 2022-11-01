from typing import Tuple

import allure
import pytest

from ui.pages.bspb.login_page import LoginPage
from ui.pages.bspb.otp_page import OtpPage


@pytest.fixture
@allure.step("Login into account")
def login(browser) -> Tuple[str, str, str]:
    """ Login into account with valid credentials """
    username = 'demo'
    password = 'demo'
    otp_code = '0000'

    with LoginPage(browser) as lp:
        lp.open(wait_page_loaded=True)
        lp.login(username, password)

    otp = OtpPage(browser)
    otp.enter_otp(otp_code)
    return username, password, otp_code
