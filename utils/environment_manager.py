from utils.get_required_env import get_required_env

ENVIRONMENT = get_required_env("ENVIRONMENT")
stage_credential = {
    "login" : get_required_env("STAGE_LOGIN"),
    "password" : get_required_env("STAGE_PASSWORD")
}

DOMAIN = f"https://{get_required_env("PROD_DOMAIN").rstrip("/")}" \
    if ENVIRONMENT == "prod" \
    else f"https://{stage_credential["login"]}:{stage_credential["password"]}@{get_required_env("STAGE_DOMAIN")}"