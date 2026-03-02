import os
import pytest
import allure
from dotenv import load_dotenv
from pages.test_api_page import YougileApi


load_dotenv()
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
COMPANY_ID = os.getenv("COMPANY_ID")
USER_ID = os.getenv("USER_ID")


@pytest.fixture()
@allure.step("Фикстура: авторизация в Yougile через API")
def yougile() -> YougileApi:
    api = YougileApi()
    with allure.step("Логинимся и получаем токен"):
        api.login(LOGIN, PASSWORD, COMPANY_ID)
    return api


@pytest.mark.api
@allure.story("Авторизация")
@allure.title("API: Логин возвращает токен")
@allure.description("""Проверяем, что после логина токен
                    сохраняется в api.token""")
@allure.severity(allure.severity_level.CRITICAL)
def test_login(yougile: YougileApi) -> None:
    with allure.step("Проверяем, что токен не None"):
        assert yougile.token is not None


@pytest.mark.api
@allure.story("Задачи")
@allure.title("API: Создание задачи")
@allure.description("""
Создаём проект → доску → колонку → задачу.
Проверяем статус-коды и что задача создалась.
                    Затем удаляем задачу (soft delete).
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_task(yougile: YougileApi) -> None:
    with allure.step("Создаём проект"):
        proj_resp = yougile.new_proj("BEST PROJECT", USER_ID)
        assert proj_resp.status_code == 201
        proj_id = proj_resp.json()["id"]

    with allure.step("Создаём доску"):
        board_resp = yougile.new_board("BEST BOARD", proj_id)
        assert board_resp.status_code == 201
        board_id = board_resp.json()["id"]

    with allure.step("Создаём колонку"):
        column_resp = yougile.new_column("BEST COLUMN", 13, board_id)
        assert column_resp.status_code == 201
        column_id = column_resp.json()["id"]

    with allure.step("Создаём задачу"):
        task_resp = yougile.new_task(
            "BEST TASK", column_id, description="TASK FOR BEST EMPLOYEE")
        assert task_resp.status_code == 201
        task_id = task_resp.json()["id"]
        assert task_id is not None

    with allure.step("Удаляем задачу (soft delete)"):
        delete_resp = yougile.delete_task(task_id)
        assert delete_resp.status_code == 200

    with allure.step("Получаем список проектов"):
        proj = yougile.get_proj()
        assert proj.status_code == 200
        proj_id = proj.json()["content"][0]["id"]

    with allure.step("Удаляем проект (soft delete)"):
        delete = yougile.delete_proj(proj_id, deleted=True)
        assert delete.status_code == 200


@pytest.mark.api
@allure.story("Задачи")
@allure.title("API: Получение задач")
@allure.description("""
Создаём проект → доску → колонку → задачу.
Затем берём список задач и проверяем, что в
                    нём есть задача с ожидаемым названием.
""")
@allure.severity(allure.severity_level.NORMAL)
def test_get_task(yougile: YougileApi) -> None:
    with allure.step("Создаём проект"):
        proj_resp = yougile.new_proj("BEST PROJECT", USER_ID)
        assert proj_resp.status_code == 201
        proj_id = proj_resp.json()["id"]

    with allure.step("Создаём доску"):
        board_resp = yougile.new_board("BEST BOARD", proj_id)
        assert board_resp.status_code == 201
        board_id = board_resp.json()["id"]

    with allure.step("Создаём колонку"):
        column_resp = yougile.new_column("BEST COLUMN", 13, board_id)
        assert column_resp.status_code == 201
        column_id = column_resp.json()["id"]

    with allure.step("Создаём задачу"):
        name = "BEST TASK"
        task_resp = yougile.new_task(name, column_id,
                                     description="TASK FOR BEST EMPLOYEE")
        assert task_resp.status_code == 201
        task_id = task_resp.json()["id"]
        assert task_id is not None

    with allure.step("Получаем список задач"):
        task_get = yougile.get_tasks()
        task_name = task_get.json()["content"][0]["title"]

    with allure.step("Проверяем, что название задачи совпадает с ожидаемым"):
        assert task_name == name

    with allure.step("Получаем список проектов"):
        proj = yougile.get_proj()
        assert proj.status_code == 200
        proj_id = proj.json()["content"][0]["id"]

    with allure.step("Удаляем проект (soft delete)"):
        delete = yougile.delete_proj(proj_id, deleted=True)
        assert delete.status_code == 200


@pytest.mark.api
@allure.story("Задачи")
@allure.title("API: Получение задачи по ID")
@allure.description("""
Создаём проект → доску → колонку → задачу.
Затем получаем задачу по id и проверяем title.
""")
@allure.severity(allure.severity_level.NORMAL)
def test_get_task_by_id(yougile: YougileApi) -> None:
    with allure.step("Создаём проект"):
        proj_resp = yougile.new_proj("NEW BEST PROJECT", USER_ID)
        assert proj_resp.status_code == 201
        proj_id = proj_resp.json()["id"]

    with allure.step("Создаём доску"):
        board_resp = yougile.new_board("NEW BEST BOARD", proj_id)
        assert board_resp.status_code == 201
        board_id = board_resp.json()["id"]

    with allure.step("Создаём колонку"):
        column_resp = yougile.new_column("NEW BEST COLUMN", 13, board_id)
        assert column_resp.status_code == 201
        column_id = column_resp.json()["id"]

    with allure.step("Создаём задачу"):
        name = "NEW BEST TASK"
        task_resp = yougile.new_task(name, column_id,
                                     description="TASK FOR BEST EMPLOYEE")
        assert task_resp.status_code == 201
        task_id = task_resp.json()["id"]

    with allure.step("Получаем задачу по id и проверяем title"):
        task_by_id = yougile.get_task_by_id(task_id)
        assert task_by_id.status_code == 200
        assert task_by_id.json()["title"] == name

    with allure.step("Получаем список проектов"):
        proj = yougile.get_proj()
        assert proj.status_code == 200
        proj_id = proj.json()["content"][0]["id"]

    with allure.step("Удаляем проект (soft delete)"):
        delete = yougile.delete_proj(proj_id, deleted=True)
        assert delete.status_code == 200


@pytest.mark.api
@allure.story("Задачи")
@allure.title("API: Удаление задачи")
@allure.description("""
Создаём задачу → удаляем её (deleted=True) →
                    проверяем, что задача помечена deleted.
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_task(yougile: YougileApi) -> None:
    with allure.step("Создаём проект"):
        proj_resp = yougile.new_proj("NEW BEST PROJECT", USER_ID)
        assert proj_resp.status_code == 201
        proj_id = proj_resp.json()["id"]

    with allure.step("Создаём доску"):
        board_resp = yougile.new_board("NEW BEST BOARD", proj_id)
        assert board_resp.status_code == 201
        board_id = board_resp.json()["id"]

    with allure.step("Создаём колонку"):
        column_resp = yougile.new_column("NEW BEST COLUMN", 13, board_id)
        assert column_resp.status_code == 201
        column_id = column_resp.json()["id"]

    with allure.step("Создаём задачу"):
        name = "NEW BEST TASK"
        task_resp = yougile.new_task(name, column_id,
                                     description="TASK FOR BEST EMPLOYEE")
        assert task_resp.status_code == 201
        task_id = task_resp.json()["id"]

    with allure.step("Удаляем задачу (soft delete)"):
        delete_resp = yougile.delete_task(task_id)
        assert delete_resp.status_code == 200

    with allure.step("Проверяем, что задача отмечена deleted=True"):
        task_after = yougile.get_task_by_id(task_id)
        assert task_after.status_code == 200
        assert task_after.json()["deleted"] is True

    with allure.step("Получаем список проектов"):
        proj = yougile.get_proj()
        assert proj.status_code == 200
        proj_id = proj.json()["content"][0]["id"]

    with allure.step("Удаляем проект (soft delete)"):
        delete = yougile.delete_proj(proj_id, deleted=True)
        assert delete.status_code == 200


@pytest.mark.api
@allure.story("Проекты")
@allure.title("API: Удаление проекта")
@allure.description("""
Получаем список проектов → берём первый →
                    удаляем его (deleted=True) → проверяем статус 200.
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_proj(yougile: YougileApi) -> None:
    with allure.step("Создаём проект"):
        proj_resp = yougile.new_proj("NEW BEST PROJECT", USER_ID)
        assert proj_resp.status_code == 201
        proj_id = proj_resp.json()["id"]

    with allure.step("Получаем список проектов"):
        proj = yougile.get_proj()
        assert proj.status_code == 200
        proj_id = proj.json()["content"][0]["id"]

    with allure.step("Удаляем проект (soft delete)"):
        delete = yougile.delete_proj(proj_id, deleted=True)
        assert delete.status_code == 200
