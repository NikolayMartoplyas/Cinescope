import re
import allure
from PageObject.base_page import BasePage


class MovieCard(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.review_field = page.get_by_placeholder("Написать отзыв")
        self.button_send = page.get_by_role("button", name="Отправить")
        self.kebab_menu = page.get_by_role("button").filter(has_text=re.compile(r"^$"))
        self.button_delete = page.get_by_role("menuitem", name="Удалить")

    @allure.step("Написание отзыва")
    def write_review(self, review):
       self.enter_text_to_element(self.review_field, review)

    @allure.step("Отправление отзыва")
    def click_button_send(self):
        self.click_element(self.button_send)

    @allure.step("удаляем отзыв")
    def delete_review(self):
        self.click_element(self.kebab_menu)
        self.click_element(self.button_delete)

    @allure.step("Проверка видимости поля для отзыва")
    def check_feedback_field(self) -> bool:
        return self.check_element(self.review_field)

    # @allure.step("Проверка видимости слова Рейтинг")
    # def check_text_rating(self) -> bool:
    #     return self.check_element(self.reviw_field)