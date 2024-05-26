from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "report" DROP COLUMN "quantity";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "report" ADD "quantity" INT NOT NULL  DEFAULT 1;"""
