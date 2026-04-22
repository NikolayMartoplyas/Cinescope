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
        self.page.goto(self.url_profile)

    @allure.step("Выход из профиля")
    def logout(self):
        self.logout_button.click()

    @allure.step("Проверка что мы вышли из профиля")
    def check_logout(self):
        expect(self.login_button).to_be_enabled()