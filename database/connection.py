import os
import redis
from tortoise import Tortoise, run_async

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_URL = f"sqlite://{BASE_DIR}/db.sqlite3"

TORTOISE_ORM_CONFIG = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(TORTOISE_ORM_CONFIG)
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(init())