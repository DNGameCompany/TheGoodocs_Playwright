# utils/user_api.py
import os

import requests
from dotenv import load_dotenv
from utils.get_required_env import get_required_env
from utils.fake_user_data import fake

load_dotenv()

GATEWAY_URL = get_required_env("GATEWAY_URL").rstrip("/")
TIMEOUT = 30
API_KEY = get_required_env("API_KEY")


def _headers(apikey: str, access_token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json", "apikey": apikey}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


def _check(response: requests.Response) -> requests.Response:
    """Кидає виняток з тілом відповіді, якщо статус 4xx/5xx."""
    if not response.ok:
        raise RuntimeError(
            f"{response.request.method} {response.url} -> "
            f"{response.status_code}: {response.text}"
        )
    return response


def authorization(email: str, password: str) -> dict:
    response = requests.post(
        f"{GATEWAY_URL}/v1/user/login",
        headers=_headers(API_KEY),
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )
    return _check(response).json()


def create_user(access_token: str, email: str, password: str) -> dict:
    response = requests.post(
        f"{GATEWAY_URL}/v1/user",
        headers=_headers(API_KEY, access_token),
        json={
            "name": "Test User (autotest)",
            "email": email,
            "password": password,
            "group_id": 3,
        },
        timeout=TIMEOUT,
    )
    return _check(response).json()

def register_user(access_token: str, email: str, password: str, verification: bool = False):
    json = {
        "name": "Test Playwright",
        "email": email,
        "password": password
    }

    if verification:
        json["verification"] = verification
        json["verification_link"] = fake.url()

    response = requests.post(
        url=f"{GATEWAY_URL}/v1/user/register-user",
        headers= _headers(API_KEY, access_token),
        json=json,
        timeout=TIMEOUT,
    )
    return _check(response).json()



def delete_user(access_token: str, user_id: int) -> dict:
    response = requests.delete(
        f"{GATEWAY_URL}/v1/user/{user_id}",
        headers=_headers(API_KEY, access_token),
        timeout=TIMEOUT,
    )
    return _check(response).json()

def get_user_id_by_email(access_token: str, email: str) -> int | None:
    """Знаходить ID користувача за його email через ендпоінт /v1/user/filter."""
    response = requests.post(
        f"{GATEWAY_URL}/v1/user/filter",
        headers=_headers(API_KEY, access_token),
        json={"email": email},
        timeout=TIMEOUT,
    )
    data = _check(response).json()

    items = data.get("data", {}).get("items", {}).get("data", [])
    for user in items:
        if user.get("email") == email:
            return user.get("id")

    return None


def delete_user_by_email(access_token: str, email: str) -> dict | None:
    """Знаходить ID користувача за email і видаляє його."""
    user_id = get_user_id_by_email(access_token, email)
    if user_id:
        return delete_user(access_token, user_id)
    return None

def filter_by_template_name(template_name: str, access_token: str) -> dict | None:
    response = requests.post(
        f"{GATEWAY_URL}/v1/templates/filter",
        headers=_headers(API_KEY, access_token),
        json={
                "search": f"{template_name}"
            },
        timeout=TIMEOUT,
    )
    return _check(response).json()
