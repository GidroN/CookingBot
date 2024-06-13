from tortoise import Tortoise, run_async
from misc.config import PG_PASSWORD, PG_DATABASE, PG_HOST, PG_PORT, PG_USER

TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": PG_DATABASE,
                "password": PG_PASSWORD,
                "host": PG_HOST,
                "port": PG_PORT,
                "user": PG_USER,
            }
        }
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(TORTOISE_ORM_CONFIG)
    # await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(init())
