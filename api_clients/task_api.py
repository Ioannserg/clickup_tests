import requests
from utils.helpers import CLICKUP_API_KEY

class TaskAPIClient:
    def __init__(self):
        self.__BASE_URL = "https://api.clickup.com/api"
        self.HEADERS = {
            "Authorization": CLICKUP_API_KEY,
            "Content-Type": "application/json"
        }

    def create_task(self, list_id, task_data):
        response_create_task = requests.post(
            f"{self.__BASE_URL}/v2/list/{list_id}/task",
            json = task_data,
            headers = self.HEADERS
        )
        return response_create_task

    def delete_task(self, task_id):
        response_delete_task = requests.delete(
            f"{self.__BASE_URL}/v2/task/{task_id}",
            headers = self.HEADERS
        )
        return response_delete_task

    def get_task(self, task_id):
        response_get_task = requests.get(
            f"{self.__BASE_URL}/v2/task/{task_id}",
            headers = self.HEADERS
        )
        return response_get_task

    def update_task(self, task_id, update_data):
        response_put_task = requests.put(
            f"{self.__BASE_URL}/v2/task/{task_id}",
            json = update_data,
            headers = self.HEADERS
        )
        return response_put_task