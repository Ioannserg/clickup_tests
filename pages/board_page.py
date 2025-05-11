from pages.base_page import BasePage
from pages.login_page import LoginPage
from tests.conftests import task_api, task_data, create_task, browser
from utils.helpers import CLICKUP_PASSWORD


class BoardPage(BasePage):
    ADD_TASK = 'button[data-test="create-task-menu__new-task-button"]'
    SHOPPING_CART_LINK_SELECTOR = '.shopping_cart_link'
    SHOPPING_CART_SELECTOR = "#shopping_cart_container"
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '90151135180/v/b/li/901510966910'

    def delete_task_for_ui(self, task_id):
        self.navigate_to()
        self.assert_element_is_visible(f'[data-id="{task_id}"]')
        self.wait_for_selector_and_click(f'[data-id="{task_id}"] >> button[class="open-task-clickable-area ng-star-inserted"]')
        self.assert_navigate_to_page(f'https://app.clickup.com/t/{task_id}')
        self.wait_for_selector_and_click('[data-test="task-view-header__task-settings"]')
        self.wait_for_selector_and_click('[data-test="dropdown-list-item__cu-task-view-menu-delete"]')
        self.assert_element_is_not_visible(f'[data-id="{task_id}"]')

    def create_task_for_ui(self, task_data):
        self.navigate_to()
        name_task = task_data.get('name')
        self.wait_for_selector_and_click(self.ADD_TASK)
        self.wait_for_selector_and_type('[data-test="draft-view__title-task"]', value=name_task, delay=100)
        self.wait_for_selector_and_click('[data-test="draft-view__quick-create-create"]')
        task_id = self.returned_task_id(name_task)
        return task_id








