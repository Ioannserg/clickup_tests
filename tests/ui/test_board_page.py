from pages.board_page import BoardPage
from tests.conftests import logged_in_page, task_api, task_data, create_task, browser
import allure


@allure.feature('Board Page Operations')
@allure.story('Комбинированные операции с задачами через UI и API')
class TestBoardPage:
    @allure.title('Создание задачи через API → Удаление через UI')
    def test_create_task_for_api_and_delete_task_for_ui(self, logged_in_page, task_api, create_task):
        task_id = create_task(list_id=901510966910).json().get('id')
        board_page = BoardPage(logged_in_page)
        board_page.delete_task_for_ui(task_id)

    @allure.title('Создание задачи через UI → Удаление через API')
    def test_create_task_for_ui_and_delete_for_api(self, logged_in_page, task_api, task_data):
        board_page = BoardPage(logged_in_page)
        task_id = board_page.create_task_for_ui(task_data)
        task_api.delete_task(task_id)

    @allure.title('Полный цикл: Создание и удаление задачи через UI')
    def test_create_task_for_ui_and_delete_for_ui(self, logged_in_page, task_data):
        board_page = BoardPage(logged_in_page)
        task_id = board_page.create_task_for_ui(task_data)
        board_page.delete_task_for_ui(task_id)