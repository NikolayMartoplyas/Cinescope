import re

import allure

from PageObject.base_page import BasePage
from faker import Faker

faker = Faker()

class MovieCard(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.reviw_field = page.get_by_role("textbox", name="Написать отзыв")
        self.button_send = page.get_by_role("button", name="Отправить")
        self.kebab_menu = page.get_by_role("button").filter(has_text=re.compile(r"^$"))
        self.button_delete = page.get_by_role("menuitem", name="Удалить")

    @staticmethod
    def review():
        return faker.paragraph(nb_sentences=2)

    @allure.step("Написание отзыва")
    def write_review(self, review):
       self.reviw_field.fill(review)

    @allure.step("Отправление отзыва")
    def click_button_send(self):
        self.button_send.click()

    @allure.step("удалияем коментарий")
    def delete_review(self):
        self.kebab_menu.click()
        self.button_delete.click()