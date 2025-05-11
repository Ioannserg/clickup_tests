import pytest
from faker import Faker
from api_clients.task_api import TaskAPIClient
from playwright.sync_api import sync_playwright, Page
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD

fake = Faker()


@pytest.fixture()
def task_data():
    return {
  "name": fake.sentence(nb_words=3),
  "description": fake.text(max_nb_chars=10)
}


@pytest.fixture(scope="session")
def task_api():
    return TaskAPIClient()

@pytest.fixture()
def create_task(task_api, task_data):
    task_ids = []

    def _create_task(list_id=901510966910, **kwargs):
        data = {**task_data, **kwargs}
        response = task_api.create_task(list_id, data)
        task_id = response.json().get('id')
        task_ids.append(task_id)
        return response

    yield _create_task


    for task_id in task_ids:
        try:
            if task_id:
                task_api.delete_task(task_id)
        except Exception as e:
            print(f"Ошибка удаления задачи: {e}")

@pytest.fixture(scope='module')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)

    yield browser

    browser.close()
    playwright.stop()


@pytest.fixture(scope='module')
def logged_in_page(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    yield page


    page.close()













