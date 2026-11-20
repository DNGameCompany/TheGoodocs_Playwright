import os
import sys

import requests

sys.path.insert(0, os.getcwd())  # щоб працював імпорт utils.*

from utils.api_requests import authorization

email = os.environ["ADMIN_EMAIL"]
password = os.environ["ADMIN_PASSWORD"]

try:
    data = authorization(
        email=email,
        password=password,
    )
except requests.exceptions.HTTPError as e:
    status = e.response.status_code if e.response is not None else "unknown"
    if status in (401, 403):
        sys.exit(
            f"[SETUP ERROR] Не вдалося авторизувати адміна ({email}): "
            f"невірний логін або пароль (HTTP {status}). Перевірте секрет ADMIN_PASSWORD."
        )
    sys.exit(f"[SETUP ERROR] Помилка HTTP {status} під час авторизації адміна: {e}")
except Exception as e:
    sys.exit(f"[SETUP ERROR] Непередбачена помилка під час авторизації адміна: {e}")

print(data["data"]["access_token"])