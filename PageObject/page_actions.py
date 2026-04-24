import allure
from playwright.sync_api import Page, expect


class PageActions:

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу")
    def open_url(self, url):
        self.page.goto(url)

    @allure.step("Ввод текста")
    def enter_text_to_element(self, locator: str, text: str):
        locator.fill(text)

    @allure.step("Клик по элементу")
    def click_element(self, locator: str):
        locator.click()

    @allure.step("Ожидание загрузки страницы")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url, timeout=10000)
        assert self.page.url == url, "Страница не загрузилась"

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible"):
        locator.wait_for(state=state, timeout=5000)

    @allure.step("Проверка видимости элемента")
    def check_element(self, locator: str):
        try:
            self.wait_for_element(locator)
            return locator.is_visible()
        except:
            return False

    @allure.step("Скриншот текущей страиницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)  # full_page=True для скриншота всей страницы

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> bool:
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            # Ждем появления элемента
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            # Ждем, пока алерт исчезнет
            notification_locator.wait_for(state="hidden")
            assert notification_locator.is_visible() == False, "Уведомление не исчезло"