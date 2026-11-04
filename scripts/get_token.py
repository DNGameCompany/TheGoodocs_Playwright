import os
import sys

sys.path.insert(0, os.getcwd())   # щоб працював імпорт utils.*

from utils.api_requests import authorization

data = authorization(
    apikey=os.environ["API_KEY"],
    email=os.environ["ADMIN_EMAIL"],
    password=os.environ["ADMIN_PASSWORD"],
)
print(data["data"]["access_token"])