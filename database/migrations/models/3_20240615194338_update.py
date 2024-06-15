from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "report" ALTER COLUMN "reason" SET NOT NULL;
        ALTER TABLE "report" ALTER COLUMN "reason" TYPE TEXT USING "reason"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "report" ALTER COLUMN "reason" TYPE VARCHAR(100) USING "reason"::VARCHAR(100);
        ALTER TABLE "report" ALTER COLUMN "reason" DROP NOT NULL;"""
