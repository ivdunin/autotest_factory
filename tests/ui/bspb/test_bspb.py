from random import choice, randint

import allure

from ui.pages.bspb.login_page import LoginPage
from ui.pages.bspb.otp_page import OtpPage
from ui.pages.bspb.payments.payments_history import PaymentsHistory
from ui.pages.bspb.payments.payments_page import PaymentsPage
from ui.pages.bspb.payments.phone_payment_page import PhonePaymentPage
from ui.pages.bspb.statement_page import StatementPage
from ui.pages.bspb.welcome_page import WelcomePage


@allure.step('Generate random phone number')
def random_phone_number() -> str:
    """ Generate valid random phone number """
    provider_codes = [925, 926, 903]
    return f'+7{choice(provider_codes)}{randint(100_00_00, 999_99_99)}'


@allure.suite("Test suite for Bank Saint-Petersburg")
class TestBankSaintPetersburg:
    def test_login(self, login, browser):
        """ Test that user:
        1. Able to login with correct credentials
        2. Able to see menu
        3. Able to open Statement page from menu
        """
        welcome = WelcomePage(browser)
        welcome.close_popup()
        assert welcome.menu_elements.count() > 0, 'No menu elements found!'
        welcome.open_statement_menu()

        statement = StatementPage(browser)
        assert statement.get_header() == 'Statement'

    def test_draft_payment(self, login, browser, faker):
        """ Test that user can make a draft phone payment.
        Payment should be visible in payments history
        """
        comment = faker.text(max_nb_chars=50)

        with allure.step('Open Payments Page'):
            payments = PaymentsPage(browser)
            payments.open(wait_page_loaded=True)
            payments.do_phone_payment()

        with allure.step('Make phone payment'):
            phone_payment = PhonePaymentPage(browser)
            phone_payment.phone_payment(random_phone_number(), amount=123, draft=True, comment=comment)

        with allure.step('Check payments history'):
            payment_history = PaymentsHistory(browser)

            found_payment = False
            history = payment_history.get_payment_history()
            for payment in history:
                if comment in payment:
                    found_payment = True

            assert found_payment, f'Payment with comment: {comment} not found in history {history}!'

    @allure.sub_suite('Invalid cases')
    def test_wrong_credentials_with_screenshot(self, browser):
        """ Test that screen sreenshot saved correctly after test is failed!

        Username: demo1
        Password: demo1
        """
        lp = LoginPage(browser)
        lp.open(wait_page_loaded=True)
        lp.login('demo1', 'demo1')

        otp = OtpPage(browser)
        otp.enter_otp('0000')
