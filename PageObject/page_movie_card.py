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
       self.enter_text_to_element(self.reviw_field, review)

    @allure.step("Отправление отзыва")
    def click_button_send(self):
        self.click_element(self.button_send)

    @allure.step("удалияем отзыв")
    def delete_review(self):
        self.click_element(self.kebab_menu)
        self.click_element(self.button_delete)

    @allure.step("Проверка видимости поля для отзыва")
    def check_feedback_field(self) -> bool:
        return self.check_element(self.reviw_field)