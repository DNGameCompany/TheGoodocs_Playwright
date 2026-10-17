from playwright.sync_api import Page, Response


def capture_ajax_response(page: Page, trigger_action, url_pattern: str = "**/ajax/category/load-more*") -> dict:
    """
    Утиліта для перехоплення Ajax-відповіді під час виконання певної дії (наприклад, кліку).

    :param page: Об'єкт сторінки Playwright
    :param trigger_action: Функція або лямбда, яка викликає Ajax (наприклад, lambda: page.click('text=Load more'))
    :param url_pattern: Шаблон URL-адреси запиту для перехоплення
    :return: Розпарсений JSON (словник) із відповіддю від сервера
    """
    try:
        # 1. Чекаємо на відповідь від сервера під час виконання дії
        with page.expect_response(url_pattern, timeout=10000) as response_info:
            trigger_action()  # Виконуємо клік або іншу дію, що запускає Ajax

        response: Response = response_info.value

        # 2. Перевіряємо статус відповіді
        if response.status == 200:
            return response.json()
        else:
            print(f"Помилка: Сервер повернув статус {response.status}")
            return {}

    except Exception as e:
        print(f"Не вдалося перехопити Ajax-запит: {e}")
        return {}
