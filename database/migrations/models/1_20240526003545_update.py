from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- ALTER TABLE "userfavouriterecipe" DROP FOREIGN KEY "fk_userfavo_recipe_06caf6f0";
        CREATE TABLE IF NOT EXISTS "report" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "quantity" INT NOT NULL  DEFAULT 1,
    "recipe_id" INT NOT NULL REFERENCES "recipe" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
        -- ALTER TABLE "userfavouriterecipe" RENAME COLUMN "receipt_id" TO "recipe_id";
        -- ALTER TABLE "userfavouriterecipe" ADD CONSTRAINT "fk_userfavo_recipe_f34b5009" FOREIGN KEY ("recipe_id") REFERENCES "recipe" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- ALTER TABLE "userfavouriterecipe" DROP FOREIGN KEY "fk_userfavo_recipe_f34b5009";
        -- ALTER TABLE "userfavouriterecipe" RENAME COLUMN "recipe_id" TO "receipt_id";
        DROP TABLE IF EXISTS "report";
        -- ALTER TABLE "userfavouriterecipe" ADD CONSTRAINT "fk_userfavo_recipe_06caf6f0" FOREIGN KEY ("receipt_id") REFERENCES "recipe" ("id") ON DELETE CASCADE;"""
