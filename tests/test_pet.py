import allure
import requests

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
