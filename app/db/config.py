import os
from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url=f"postgres://{os.getenv("DB_USER")}:{os.getenv("DB_PWD")}@{os.getenv("DB_HOST")}:{
            os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}",
        modules={"models": ["app.db.models"]},
    )

    await Tortoise.generate_schemas()
