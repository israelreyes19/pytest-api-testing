import os

HOST = os.getenv("APP_HOST", "http://localhost:3000")

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "mysecrettoken")

ENV_PATH_MAP = {
    "dev": "/dev",
    "prod": "/prod",
}

def get_base_url(env: str) -> str:
    env = env.lower()
    if env not in ENV_PATH_MAP:
        raise ValueError(f"Environment '{env}' not valid")
    
    return f"{HOST.rstrip('/')}{ENV_PATH_MAP[env]}"