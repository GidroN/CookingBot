import os
from tortoise import Tortoise, run_async
from misc.config import PG_PASSWORD, PG_DATABASE, PG_HOST, PG_PORT, PG_USER

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_URL = f"sqlite://{BASE_DIR}/db.sqlite3"

TORTOISE_ORM_CONFIG = {
    "connections": {
        "postgres": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": PG_DATABASE,
                "password": PG_PASSWORD,
                "host": PG_HOST,
                "port": PG_PORT,
                "user": PG_USER,
            }
        },
        'sqlite': DB_URL,
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "postgres",
        },
    },
}


async def init(generate_schemas: bool = True):
    await Tortoise.init(TORTOISE_ORM_CONFIG)
    if generate_schemas:
        await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(init())
