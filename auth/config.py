import os
from pathlib import Path
from urllib.parse import quote_plus


def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file()


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_database_url() -> str:
    driver = os.environ.get("DB_DRIVER", "mysql+pymysql")
    username = get_required_env("DB_USERNAME")
    password = quote_plus(get_required_env("DB_PASSWORD"))
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "3306")
    database = get_required_env("DB_NAME")

    return f"{driver}://{username}:{password}@{host}:{port}/{database}"
