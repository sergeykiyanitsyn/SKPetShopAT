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