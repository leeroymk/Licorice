import asyncio
import logging
import schedule
import time
from app.main import main


def job():
    logging.info("Запускаем парсинг криптовалют")
    asyncio.run(main())


def run_scheduler():
    schedule.every().hour.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
