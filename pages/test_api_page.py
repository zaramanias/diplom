import requests
import allure

base_url = "https://yougile.com/api-v2"


class YougileApi:
    def __init__(self) -> None:
        """
        Конструктор класса YougileApi
        """
        self.token: str | None = None
        self.headers: dict[str, str] = {}

    @allure.step("""API: Логин в Yougile
                 (ID компании={company_id}, логин={login})""")
    def login(self, login: str, password: str,
              company_id: str) -> requests.Response:
        """
        Логин в Yougile
        """
        resp = requests.post(f"{base_url}/auth/keys/get", json={
            "login": login, "password": password, "companyId": company_id})
        self.token = resp.json()[0]["key"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        return resp

    @allure.step("API: Получить проекты {proj_id}")
    def get_proj(self, proj_id: str | None = None) -> requests.Response:
        """
        Получение проекта
        """
        if proj_id:
            url = f"{base_url}/projects/{proj_id}"
        else:
            url = f"{base_url}/projects"
        resp = requests.get(url, headers=self.headers)
        return resp

    @allure.step("""API: Создать проект с названием: {title},
                 юзерайди: {user_id})""")
    def new_proj(self, title: str, user_id: str) -> requests.Response:
        """
        Создание проекта
        """
        resp = requests.post(f"{base_url}/projects", json={
            "title": title, "users": {user_id: "admin"}}, headers=self.headers)
        return resp

    @allure.step("""API: Создать доску с названием: {title},
                 проджектайди: {proj_id}""")
    def new_board(self, title: str, proj_id: str) -> requests.Response:
        """
        Создание доски
        """
        resp = requests.post(f"{base_url}/boards", json={
            "title": title, "projectId": proj_id}, headers=self.headers)
        return resp

    @allure.step("""API: Создать колонку
                 (Навание: {title}, цвет: {color}, айди доски: {board_id})""")
    def new_column(self, title: str,
                   color: int, board_id: str) -> requests.Response:
        """
        Создание колонки
        """
        resp = requests.post(f"{base_url}/columns", json={
            "title": title, "color": color, "boardId": board_id},
            headers=self.headers)
        return resp

    @allure.step("""API: Создать задачу с названием {title},
                 айди колонки {column_id}""")
    def new_task(self, title: str, column_id: str,
                 description: str = "") -> requests.Response:
        """
        Создание задачи
        """
        resp = requests.post(f"{base_url}/tasks", json={
            "title": title, "columnId": column_id, "description": description},
            headers=self.headers)
        return resp

    @allure.step("API: Получить список задач /task-list")
    def get_tasks(self) -> requests.Response:
        """
        Получение списка задач
        """
        resp = requests.get(f"{base_url}/task-list", headers=self.headers)
        return resp

    @allure.step("API: Получить задачу по айди: {id}")
    def get_task_by_id(self, id: str) -> requests.Response:
        """
        Получение списка задач по айди
        """
        resp = requests.get(f"{base_url}/tasks/{id}", headers=self.headers)
        return resp

    @allure.step("API: Удалить задачу по айди: {id}")
    def delete_task(self, id: str) -> requests.Response:
        """
        Удалить задачу по айди
        """
        resp = requests.put(f"{base_url}/tasks/{id}",
                            json={"deleted": True}, headers=self.headers)
        return resp

    @allure.step("API: Удалить проект с айди {proj_id}, удален {deleted}")
    def delete_proj(self, proj_id: str,
                    deleted: bool = True) -> requests.Response:
        """
        Удалить проект по айди
        """
        resp = requests.put(f"{base_url}/projects/{proj_id}", json={
            "deleted": deleted}, headers=self.headers)
        return resp
