from tests.conftests import create_task, task_api, task_data, fake
import pytest
import allure

@allure.feature('Task API CRUD Operations')
@allure.story('Позитивные тесты')
class TestTaskAPIPositive:
    @allure.title('Создание новой задачи с валидными данными')
    @allure.description('Проверка успешного создания задачи через API')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_task(self, create_task, task_data):
        with allure.step('1. Создание задачи через фикстуру'):
            response = create_task()
            response_data = response.json()

        with allure.step('2. Проверка ответа'):
            allure.attach(str(response.status_code), name='Status Code')
            allure.attach(str(response_data), name='Response Body')
            assert response.status_code == 200
            assert response_data.get('id') is not None
            assert response_data['name'] == task_data['name']
            assert response_data['description'] == task_data['description']

    @allure.title('Обновление существующей задачи')
    @allure.description('Проверка обновления названия и описания задачи')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_task(self, task_api, create_task):
        with allure.step('1. Создание тестовой задачи'):
            create_response = create_task()
            task_id = create_response.json().get('id')

        with allure.step('2. Подготовка новых данных'):
            new_data = {
                "name": fake.sentence(nb_words=10),
                "description": fake.text(max_nb_chars=100)
            }
            allure.attach(str(new_data), name='New Task Data')

        with allure.step('3. Отправка запроса на обновление'):
            update_response = task_api.update_task(task_id, new_data)
            updated_data = update_response.json()

        with allure.step('4. Проверка результатов'):
            assert update_response.status_code in [200, 201]
            assert updated_data['id'] == task_id
            assert updated_data['name'] == new_data['name']
            assert updated_data['description'] == new_data['description']

    @allure.title('Получение информации о задаче')
    @allure.description('Проверка корректности данных при получении задачи')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_task(self, task_api, create_task):
        with allure.step('1. Создание тестовой задачи'):
            new_task = create_task()
            created_data = new_task.json()
            task_id = created_data.get('id')

        with allure.step('2. Получение задачи по ID'):
            response = task_api.get_task(task_id)
            response_data = response.json()

        with allure.step('3. Сравнение данных'):
            assert response.status_code == 200
            assert created_data['name'] == response_data['name']
            assert created_data['description'] == response_data['description']


@allure.feature('Task API CRUD Operations')
@allure.story('Негативные тесты')
class TestTaskAPINegative:
    @allure.title('Попытка создания задачи с невалидными данными')
    @allure.description('Параметризированный тест с различными невалидными сценариями')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("list_id, invalid_data, expected_status, error_key", [
        (901510804296, {}, 400, "err"),
        (901510804296, {"description": "Только описание"}, 400, "name"),
        (901510804296, {"name": "Тест", "priority": "высокий"}, 400, "Priority invalid"),
        (901510804296, {"name": f"{[x for x in range(0, 4001)]}"}, 400, "name"),
        (100000000001, {"name": "Тест инвалидного листа"}, 401, "Team not authorized")
    ])
    def test_create_task_negative(self, task_api, list_id, invalid_data, expected_status, error_key):
        with allure.step(f'Попытка создания с невалидными данными: {error_key}'):
            allure.attach(str(invalid_data), name='Invalid Data')
            response = task_api.create_task(list_id=list_id, task_data=invalid_data)

            with allure.step('Проверка ответа'):
                assert response.status_code == expected_status
                assert error_key in str(response.json())

    @allure.title('Попытка получения несуществующей задачи')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_task_negative(self, task_api, create_task):
        with allure.step('1. Попытка получить задачу с невалидным ID'):
            response = task_api.get_task('TEST')
            assert response.status_code == 401

        with allure.step('2. Попытка получить удаленную задачу'):
            new_task = create_task()
            task_id = new_task.json().get('id')
            task_api.delete_task(task_id)
            response = task_api.get_task(task_id)
            assert response.status_code == 404

    @allure.title('Попытка обновления с невалидными данными')
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_task_negative(self, task_api, create_task):
        with allure.step('1. Создание тестовой задачи'):
            task = create_task()
            task_id = task.json().get('id')

        with allure.step('2. Невалидное обновление: числовое имя'):
            response = task_api.update_task(task_id, {"name": 123123123})
            assert response.status_code == 400

        with allure.step('3. Невалидное обновление: слишком длинное описание'):
            response = task_api.update_task(task_id, {"description": f'{[x for x in range(0, 1000000)]}'})
            assert response.status_code == 413

    @allure.title('Попытка удаления несуществующей задачи')
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_task_negative(self, task_api):
        with allure.step('Попытка удаления задачи с несуществующим ID'):
            response = task_api.delete_task('123123123123')
            assert response.status_code == 401
