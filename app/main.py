import asyncio
import datetime

from tortoise import Tortoise

from app.db.config import init_db
from app.db.db_mgmt import compare_price, get_previous_price, save_to_db

from app.services.exchange_api import get_all_prices
from app.services.smtp import send_email
from app.utils import form_message, get_total_cash, write_to_csv, setup_logging


setup_logging()


async def main():
    await init_db()
    pairs = ["BTC/USDT", "BTC/ETH", "BTC/XMR", "BTC/SOL", "BTC/RUB", "BTC/DOGE"]

    message_dict = {}

    for pair in pairs:
        current_min_price, current_max_price, exchange = await get_all_prices(pair)
        previous_price = await get_previous_price(pair)
        difference = await compare_price(current_max_price, previous_price)
        total_cash = get_total_cash(current_max_price)
        current_date = datetime.datetime.now()

        if difference >= 0.03:
            message = form_message(pair, current_max_price, difference, total_cash)
            message_dict[pair] = message

        if difference > 0:
            write_to_csv(
                pair, current_max_price, current_min_price, current_date, difference, total_cash
            )

        await save_to_db(pair, current_min_price, current_max_price, exchange, current_date)

    subject_pairs = ", ".join(message_dict.keys())
    subject = f"Изменение в цене валют {subject_pairs}"
    message = "\n".join(message_dict.values())
    send_email(subject, message)

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
