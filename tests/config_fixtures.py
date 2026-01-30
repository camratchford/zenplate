from pathlib import Path

from zenplate.config import ZenplateConfig

project_root = Path(__file__).parent.parent
fixtures = project_root / "tests" / "fixtures"


def new_config():
    return ZenplateConfig()
