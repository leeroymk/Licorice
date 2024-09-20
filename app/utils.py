import csv
import os
import logging
from logging.handlers import RotatingFileHandler


def write_to_csv(pair, current_max_price, current_min_price, current_date, difference, total_cash):
    filename = "currencies.csv"
    fieldnames = [
        "title",
        "price",
        "max price",
        "min price",
        "date ISOformat",
        "difference",
        "total amount",
    ]

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "title": pair,
                "price": current_max_price,
                "max price": current_max_price,
                "min price": current_min_price,
                "date ISOformat": current_date,
                "difference": difference,
                "total amount": total_cash,
            }
        )


def setup_logging():
    log_handler = RotatingFileHandler("logs.log", maxBytes=10 * 1024 * 1024, backupCount=5)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
    )
    log_handler.setFormatter(formatter)

    logging.getLogger().addHandler(log_handler)
    logging.getLogger().setLevel(logging.INFO)

    return log_handler


def get_total_cash(current_price):
    # По условиям у Лакрицы 3 BTC
    return 3 * current_price


def form_message(pair, current_price, difference, total_cash):
    message = (
        f"Цена для пары {pair} изменилась на {difference:.3f}%\n"
        f"Текущая цена {current_price:.3f}\n"
        f"Ваши накопления {total_cash}"
    )
    return message
