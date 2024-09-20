import os
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise

from app.api.crud import (
    create_currency_pair,
    delete_currency_pair,
    get_all_currency_pairs,
    get_currency_pair,
    update_currency_pair,
)


app = web.Application()


app.router.add_post("/currency_pairs/", create_currency_pair)
app.router.add_get("/currency_pairs/", get_all_currency_pairs)
app.router.add_get("/currency_pairs/{pair_id}", get_currency_pair)
app.router.add_put("/currency_pairs/{pair_id}", update_currency_pair)
app.router.add_delete("/currency_pairs/{pair_id}", delete_currency_pair)


register_tortoise(
    app,
    db_url=f"postgres://{os.getenv("DB_USER")}:{os.getenv("DB_PWD")}@{os.getenv("DB_HOST")}:{
            os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}",
    modules={"models": ["app.db.models"]},
    generate_schemas=True,
)


if __name__ == "__main__":
    web.run_app(app)
