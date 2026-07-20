import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статус ответа"):
            assert response.status_code == 200, f"Ожидался статус кода 200, а пришел {response.status_code}"

        with allure.step("Проверка текстового содержания ответа"):
            assert response.text == "Pet deleted", f"Ожидался текст 'Pet deleted', а пришел {response.text}"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available",
            }

            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статус ответа"):
            assert response.status_code == 404, f"Ожидался статус кода 404, а пришел {response.status_code}"

        with (allure.step("Проверка текстового содержания ответа")):
            assert response.text == "Pet not found", f"Ожидался текст 'Pet not found', а пришел {response.text}"

    @allure.title("Попытка получить данные несуществующего питомца")
    def test_get_nonexistent_pet(self):
        with allure.step("Получение запроса несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статус ответа"):
            assert response.status_code == 404, f"Ожидался статус кода 404, а пришел {response.status_code}"

        with (allure.step("Проверка текстового содержания ответа")):
            assert response.text == "Pet not found", f"Ожидался текст 'Pet not found', а пришел {response.text}"

    @allure.title("Создание нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "Бублик",
                "status": "available",
            }

        with allure.step("Отправка запроса POST на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON-схемы"):
            assert response.status_code in (200,
                                            201), f"Ожидался 200-201 статус коды, а пришел статус код {response.status_code}"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка парамтров питомца в ответе"):
            assert response_json["id"] == payload["id"], f"id питомца отличается от {payload["id"]}"
            assert response_json["name"] == payload["name"], f"Имя питомца отличается от {payload["name"]}"
            assert response_json["status"] == payload["status"], f"Статус питомца отличается от {payload["status"]}"

    @allure.title("Создание нового питомца Собакинс")
    def test_add_pet_dog(self):
        with allure.step("Подготовка данных для создания собаки"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags":
                    [
                        {
                            "id": 0,
                            "name": "string"
                        }
                    ],
                "status": "available"
            }

        with allure.step("Отправка запроса POST на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON-схемы"):
            assert response.status_code in (200,
                                            201), f"Ожидался 200-201 статус коды, а пришел статус код {response.status_code}"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка id питомца в ответе"):
            assert response_json["id"] == payload["id"], f"id питомца отличается от {payload["id"]}"

        with allure.step("Проверка Имени питомца в ответе"):
            assert response_json["name"] == payload["name"], f"Имя питомца отличается от {payload["name"]}"

        with allure.step("Проверка Категории питомца в ответе"):
            assert response_json["category"] == payload["category"]

        with allure.step("Проверка Ссылок фотографий питомца в ответе"):
            assert response_json["photoUrls"] == payload["photoUrls"]

        with allure.step("Проверка тэгов питомца в ответе"):
            assert response_json["tags"] == payload["tags"]

        with allure.step("Проверка Статуса питомца в ответе"):
            assert response_json["status"] == payload["status"], f"Статус питомца отличается от {payload["status"]}"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet_by_id(self, create_pet):
        with allure.step("Получение созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления"):
            pet_for_update = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на изменение информации о питомце по ID"):
            response = requests.put(url=f"{BASE_URL}/pet", json=pet_for_update)

        with allure.step("Проверка статуса ответа и обновление данных питомца"):
            assert response.status_code == 200
            response_json = response.json()
            assert response_json["id"] == pet_for_update["id"]
            assert response_json["name"] == pet_for_update["name"]
            assert response_json["status"] == pet_for_update["status"]

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Удаление питомца по ID"):
            requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step(f"Отправка запроса GET по ID {pet_id}"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            response.status_code = 404