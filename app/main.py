from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url="postgres://user:password@localhost:5432/dbname",
        modules={"models": ["app.models"]},
    )
    await Tortoise.generate_schemas()
