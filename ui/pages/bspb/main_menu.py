from ui.page_object import BasePage
from ui.page_object import PageElement, PageElements
from ui.page_object import by_id, by_css


class MainMenu(BasePage):
    menu_elements = PageElements(by_css('ul.navigation-menu.nav > li'))
    accounts_menu = PageElement(by_id('accounts'))
    statement_menu = PageElement(by_id('statement'))

    def open_statement_menu(self):
        self.accounts_menu.mouse_over()
        self.statement_menu.click()
