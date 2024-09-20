import asyncio
import schedule
import time


def job():
    asyncio.run(())


schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
