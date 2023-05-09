import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigurationsManager:

    def __init__(self) -> None:
        self.pytest_plugins = list()

    def local_load_dotenv(self):
        ENV_FILE_PATH = BASE_DIR / '.env'
        if os.getenv('CI', False) is False and ENV_FILE_PATH.exists():
            load_dotenv(str(ENV_FILE_PATH))
