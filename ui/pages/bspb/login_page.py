from ui.page_object import PageElement
from ui.page_object import by_css, by_id
from ui.pages.bspb.bspb import BSPB


class LoginPage(BSPB):
    username: PageElement = PageElement(by_css('#login-form input[name="username"]'))
    password: PageElement = PageElement(by_css('#login-form input[name="password"]'))
    btn_login: PageElement = PageElement(by_id('login-button'))

    def login(self, username: str, password: str):
        self.username.send_keys(username, clear=True)
        self.password.send_keys(password, clear=True)
        self.btn_login.click()
