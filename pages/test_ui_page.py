import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


base_url = "https://www.labirint.ru/"
cart_url = "https://www.labirint.ru/cart/"


class LabirintPage:
    """
    Page Object для сайта labirint.ru
    """

    # ЛОКАТОРЫ
    search_input = (By.ID, "search-field")
    search_btn = (By.CSS_SELECTOR, "button.b-header-b-search-e-btn")
    search_result_title = (By.CSS_SELECTOR, "h1.index-top-title")
    product_card = (By.CSS_SELECTOR, ".product-card")
    product_btn_to_cart = (By.CSS_SELECTOR, "a.btn-tocart")
    cart_count = (By.CSS_SELECTOR, "span.j-cart-count")
    cart_minus_btn = (By.CSS_SELECTOR, ".book-buttons .counter-add-minus")
    product_name = (By.CSS_SELECTOR, "a.product-card__name")
    product_name_in_card = (By.CSS_SELECTOR, "h1")
    restore_btn = (By.CSS_SELECTOR, "a.b-link-popup.g-alttext-deepblue")
    delete_cart = (By.CSS_SELECTOR,
                   "div.text-regular.empty-basket-link.trash-link "
                   "span.b-link-popup.basket-header-links"
                   )

    def __init__(self) -> None:
        """
        Конструктор класса LabirintPage
        """
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    @allure.step("Открытие главной страницы")
    def open(self) -> None:
        """
        Открывает главную страницу и добавляет куки
        """
        self.driver.get(base_url)
        self.driver.add_cookie({
            "name": "cookie_policy",
            "value": "1"
            })

    @allure.step("Открытие страницы корзины")
    def open_cart(self) -> None:
        """
        Открывает страницу корзины.
        """
        self.driver.get(cart_url)

    def quit(self) -> None:
        self.driver.quit()

    @allure.step("Поиск по запросу: {text}")
    def search(self, text: str) -> None:
        """
        Выполняет поиск по введенному тексту.
        :param text: str - строка поиска
        """
        self.wait.until(EC.visibility_of_element_located(
            self.search_input)).send_keys(text)
        self.wait.until(EC.element_to_be_clickable(self.search_btn)).click()

    @allure.step("Получение заголовка выдачи поиска")
    def get_search_result(self) -> str:
        """
        Возвращает заголовок выдачи (data-title).
        :return: str
        """
        element = self.wait.until(
            EC.visibility_of_element_located(self.search_result_title)
        )
        return element.get_attribute("data-title")

    @allure.step("Добавление товара в корзину по индексу")
    def add_product(self, index: int) -> None:
        """
        Добавляет товар в корзину по индексу карточки.
        :param index: int - индекс карточки
        """
        cards = self.wait.until(
            EC.presence_of_all_elements_located(self.product_card)
        )
        cards[index].find_element(*self.product_btn_to_cart).click()
        self.wait.until(
            EC.text_to_be_present_in_element(self.cart_count, "1")
        )

    @allure.step("Получение количества товаров в корзине (счётчик в шапке)")
    def get_cart_count(self) -> int:
        """
        Возвращает количество товаров в корзине по счетчику в шапке.
        :return: int
        """
        element = self.driver.find_element(*self.cart_count).text.strip()
        return int(element)

    @allure.step("Нажатие '-' в корзине")
    def click_btn_minus_in_cart(self) -> None:
        """
        Уменьшает количество товара в корзине.
        """
        self.driver.find_element(*self.cart_minus_btn).click()

    @allure.step("Подтверждение alert (OK) при удалении")
    def confirm_alert_ok(self) -> None:
        """
        Подтверждает alert и ждёт, что корзина станет пустой.
        """
        self.wait.until(EC.alert_is_present()).accept()
        self.wait.until(
            EC.text_to_be_present_in_element(self.cart_count, "0")
        )

    @allure.step("Открытие карточки товара по индексу")
    def open_prod_card(self, index: int) -> None:
        """
        Открывает карточку товара по индексу карточки.
        :param index: int
        """
        cards = self.wait.until(
            EC.presence_of_all_elements_located(self.product_card)
        )
        cards[index].find_element(*self.product_name).click()

    @allure.step("Получение названия книги из выдачи по индексу")
    def get_name_in_search(self, index: int) -> str:
        """
        Возвращает название книги в поисковой выдаче по индексу карточки.
        :return: str
        """
        cards = self.wait.until(
            EC.presence_of_all_elements_located(self.product_card)
        )
        name = cards[index].find_element(*self.product_name).text.strip()
        return name

    @allure.step("Получение названия книги на странице карточки")
    def get_name_in_card(self) -> str:
        """
        Возвращает название книги на странице карточки товара.
        Отрезаем автора по ':' (как ты делал).
        :return: str
        """
        name = self.driver.find_element(
            *self.product_name_in_card).text.strip()
        return name.split(":")[0].strip()

    @allure.step("Очистка корзины (кнопка 'Очистить корзину')")
    def delete_from_cart(self) -> None:
        """
        Нажимает 'Очистить корзину' на странице корзины.
        """
        self.wait.until(
            EC.visibility_of_element_located(self.delete_cart)).click()

    @allure.step("Восстановление удаленных товаров в корзине")
    def restore_cart(self) -> None:
        """
        Нажимает 'Восстановить удаленное' и ждёт,
        что в корзине снова будет >0 товаров.
        """
        self.wait.until(
            EC.visibility_of_element_located(self.restore_btn)).click()
        self.wait.until(EC.text_to_be_present_in_element(self.cart_count, "1"))
