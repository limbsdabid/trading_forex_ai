import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "config.json"
DATA_DIR = PROJECT_ROOT / "data"


def load_config(config_path=CONFIG_PATH):
    if not config_path.exists():
        raise FileNotFoundError(
            f"Missing {config_path.name}. Copy config.example.json to config.json "
            "and add your local MT5 demo credentials."
        )

    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
