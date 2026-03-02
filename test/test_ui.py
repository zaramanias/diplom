from pages.test_ui_page import LabirintPage
import pytest
import allure


@pytest.mark.ui
@allure.story("Поиск товаров")
@allure.title("UI: Поиск возвращает результаты")
@allure.description(
    "Проверяем, что поиск по запросу отображает корректные данные.")
@allure.severity(allure.severity_level.NORMAL)
def test_search() -> None:
    page = LabirintPage()
    with allure.step("Открытие страницы"):
        page.open()
    search_words = "java"
    with allure.step(f"выполняем поиск по запросу '{search_words}'"):
        page.search(search_words)
    with allure.step("Получаем заголовок выдачи с введенным запросом"):
        search_response = page.get_search_result()
    with allure.step("Сравниваем то что мы вводили с тем что получили"):
        assert search_words == search_response
    with allure.step("Закрытие браузера"):
        page.quit()


@pytest.mark.ui
@allure.story("Работа с корзиной")
@allure.title("UI: Добавление товара в корзину")
@allure.description("""
                    Проверяем, что при добавлении
                    товаров количество в корзине увеличивается.
                    """)
@allure.severity(allure.severity_level.CRITICAL)
def test_add_to_cart() -> None:
    page = LabirintPage()
    with allure.step("Открытие страницы"):
        page.open()
    search_words = "java"
    with allure.step(f"выполняем поиск по запросу '{search_words}'"):
        page.search(search_words)
    with allure.step("Получаем количество книг в корзине до добавления"):
        before = page.get_cart_count()
    with allure.step("Добавляем книги с индексом 5,3 и 4 в корзину"):
        page.add_product(5)
        page.add_product(3)
        page.add_product(4)
    with allure.step("Получаем количество книг в корзине после добавления"):
        after = page.get_cart_count()
    with allure.step("Сравниваем количество ДО с количеством ПОСЛЕ"):
        assert after > before
    with allure.step("Закрытие браузера"):
        page.quit()


@pytest.mark.ui
@allure.story("Работа с корзиной")
@allure.title("UI: Удаление товара из корзины через кнопку '-'")
@allure.description("""
                    Проверяем, что удаление товара из корзины
                    через '-' приводит к пустой корзине.
                    """)
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_prod_with_minus() -> None:
    page = LabirintPage()
    with allure.step("Открытие страницы"):
        page.open()
    search_words = "java"
    with allure.step(f"выполняем поиск по запросу '{search_words}'"):
        page.search(search_words)
    with allure.step("Добавляем товар с индексом 5 в корзину"):
        page.add_product(5)
    with allure.step("Открываем страницу корзины"):
        page.open_cart()
    with allure.step("Нажимаем '-' для удаления товара"):
        page.click_btn_minus_in_cart()
    with allure.step("Подтверждаем удаление в alert"):
        page.confirm_alert_ok()
    with allure.step("Проверяем, что корзина пустая"):
        total = page.get_cart_count()
        assert total == 0
    with allure.step("Закрытие браузера"):
        page.quit()


@pytest.mark.ui
@allure.story("Карточка товара")
@allure.title("UI: Клик по карточке товара открывает корректную карточку")
@allure.description("""
                    Проверяем, что название книги в выдаче
                    совпадает с названием на странице карточки товара.
                    """)
@allure.severity(allure.severity_level.NORMAL)
def test_open_prod_card() -> None:
    page = LabirintPage()
    with allure.step("Открытие страницы"):
        page.open()
    search_words = "java"
    with allure.step(f"Выполняем поиск по запросу '{search_words}'"):
        page.search(search_words)
    with allure.step("Получаем название книги с индексом 4"):
        name_in_search = page.get_name_in_search(4)
    with allure.step("Открываем карточку товара в выдаче по индексу 4"):
        page.open_prod_card(4)
    with allure.step("Получаем название книги на странице карточки"):
        name_in_card = page.get_name_in_card()
    with allure.step("Сравниваем название из выдачи с названием в карточке"):
        assert name_in_search == name_in_card
    with allure.step("Закрытие браузера"):
        page.quit()


@pytest.mark.ui
@allure.story("Работа с корзиной")
@allure.title("UI: Восстановление корзины после удаления")
@allure.description("""
    Проверяем, что после очистки корзины можно восстановить
    удаленные товары через кнопку 'Восстановить удаленное',
    и количество товаров увеличивается.""")
@allure.severity(allure.severity_level.CRITICAL)
def test_restore_prod_in_cart() -> None:
    page = LabirintPage()
    with allure.step("Открытие страницы"):
        page.open()
    search_words = "java"
    with allure.step(f"Выполняем поиск по запросу '{search_words}'"):
        page.search(search_words)
    with allure.step("Добавляем товар с индексом 5 в корзину"):
        page.add_product(5)
    with allure.step("Открываем страницу корзины"):
        page.open_cart()
    with allure.step("Очищаем корзину с кнопкой 'Очистить корзину'"):
        page.delete_from_cart()
    with allure.step("Фиксируем количество товаров в корзине после удаления"):
        prod_before_restore = page.get_cart_count()
    with allure.step("Восстанавливаем удаленные товары"):
        page.restore_cart()
    with allure.step("""
                     Фиксируем количество товаров в корзине
                     после восстановления
                     """):
        prod_after_restore = page.get_cart_count()
    with allure.step("Количество товаров ПОСЛЕ восстановления больше чем ДО"):
        assert prod_after_restore > prod_before_restore
    with allure.step("Закрытие браузера"):
        page.quit()
