from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(60) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "tg_id" VARCHAR(10) NOT NULL UNIQUE,
    "username" VARCHAR(32),
    "name" VARCHAR(129) NOT NULL
);
CREATE TABLE IF NOT EXISTS "receipt" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(60) NOT NULL,
    "url" VARCHAR(150) NOT NULL,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE,
    "creator_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "userfavouritereceipt" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "receipt_id" INT NOT NULL REFERENCES "receipt" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
