from pages.login_page import LoginPage
from tests.conftests import browser
from utils.helpers import CLICKUP_PASSWORD, CLICKUP_EMAIL
import allure

@allure.feature('Авторизация')
@allure.story('Проверка процесса входа в систему')
class TestLoginPage:

    @allure.title('Успешная авторизация с валидными данными')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_process(self, browser):
        with allure.step('Открыть страницу авторизации'):
            page = browser.new_page()
            login_page = LoginPage(page)

        with allure.step('Ввести корректные учетные данные'):
            login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

        with allure.step('Закрыть страницу'):
            page.close()


    @allure.title('Неуспешная авторизация с неверным паролем')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_negative_login_process(self, browser):
        with allure.step('Открыть страницу авторизации'):
            page = browser.new_page()
            login = LoginPage(page)
        with allure.step('2. Ввести неверный пароль'):
            login.login_negative(CLICKUP_EMAIL, '12345677')

        with allure.step('Закрыть страницу'):
            page.close()







