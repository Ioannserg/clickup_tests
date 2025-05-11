from playwright.sync_api import sync_playwright, expect


class BasePage:
    __BASE_URL = 'https://app.clickup.com'

    def __init__(self, page):
        self.page = page
        self._endpoint = ''

    def _get_full_url(self):
        return f'{self.__BASE_URL}/{self._endpoint}'

    def navigate_to(self):
        full_url = self._get_full_url()
        self.page.goto(full_url)
        self.page.wait_for_load_state('load')
        expect(self.page).to_have_url(full_url)


    def wait_for_selector_and_type(self, selector, value, delay):
        self.page.wait_for_selector(selector)
        self.page.type(selector, value, delay=delay)


    def wait_for_selector_and_fill(self, selector, value):
        self.page.wait_for_selector(selector)
        self.page.fill(selector, value)

    def wait_for_selector_and_click(self, selector):
        self.page.wait_for_selector(selector, timeout=30000)
        self.page.click(selector)

    def assert_element_is_visible(self, selector):
        expect(self.page.locator(selector)).to_be_visible(timeout=30000)

    def assert_text_present_on_page(self, text):
        expect(self.page.locator("body")).to_contain_text(text)

    def assert_text_in_element(self, selector, text):
        expect(self.page.locator(selector)).to_have_text(text)

    def assert_input_value(self, selector, expected_value):
        expect(self.page.locator(selector)).to_have_value(expected_value)

    def assert_navigate_to_page(self, url):
        self.page.wait_for_url(url)
        expect(self.page).to_have_url(url, timeout=60000)

    def assert_element_is_not_visible(self, selector):
        expect(self.page.locator(selector)).not_to_be_visible()

    def returned_task_id(self, task_name):
        task_name_locator = self.page.locator(
            f'.board-task__name-link.ng-star-inserted:has-text("{task_name}")'
        )
        task_item_locator = task_name_locator.locator(
            'xpath=ancestor::*[contains(@class, "board-group__task-list-item") and @data-id]'
        )
        task_id = task_item_locator.get_attribute('data-id')
        return task_id


