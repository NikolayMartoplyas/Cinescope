import allure

from PageObject.base_page import BasePage
from playwright.sync_api import Page, expect


class PageProfile(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.url_profile = f"{self.base_url}profile"
        self.logout_button = page.get_by_role("button", name="Выход")
        self.login_button = page.get_by_role("button", name="Войти")


    @allure.step("Вход на страницу профиля")
    def open_page_profile(self):
        self.open_url(self.url_profile)

    @allure.step("Выход из профиля")
    def logout(self):
        self.click_element(self.logout_button)

    @allure.step("Проверка что мы вышли из профиля")
    def check_logout(self):
        self.check_element(self.login_button)