from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "recipe" ADD "is_active" INT NOT NULL  DEFAULT 1;
        ALTER TABLE "user" ADD "warnings" INT NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "recipe" DROP COLUMN "is_active";
        ALTER TABLE "user" DROP COLUMN "warnings";"""
