from pathlib import Path

from zenplate.config import Config

project_root = Path(__file__).parent.parent
fixtures = project_root / "tests" / "fixtures"


def new_config():
    return Config()
