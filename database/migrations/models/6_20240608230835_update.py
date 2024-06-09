from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "userwarn" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "reason" VARCHAR(100) NOT NULL,
    "admin_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "recipe_id" INT NOT NULL REFERENCES "recipe" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "userwarn";"""
