from app.db.models import CurrencyPair


async def save_to_db(pair, min_price, current_max_price, exchange, current_date):
    record, created = await CurrencyPair.get_or_create(
        pair=pair,
        defaults={
            "exchange": exchange,
            "price": current_max_price,
            "date": current_date,
            "min_price": min_price,
            "max_price": current_max_price,
        },
    )

    if not created:
        record.price = current_max_price
        record.min_price = await check_min_price(pair, min_price)
        record.max_price = await check_max_price(pair, current_max_price)
        record.exchange = exchange
        record.date = current_date

        await record.save()


async def get_previous_price(pair):
    db_pair = await CurrencyPair.get_or_none(pair=pair)
    if db_pair is not None:
        return db_pair.price
    return None


async def compare_price(current_price, previous_price):
    if previous_price is None:
        return 0

    price_difference = ((current_price - previous_price) / previous_price) * 100
    return price_difference


async def check_min_price(pair, new_min_price):
    row = await CurrencyPair.get_or_none(pair=pair)
    if row.min_price is None or new_min_price < row.min_price:
        row.min_price = new_min_price
        return new_min_price
    return None


async def check_max_price(pair, new_max_price):
    row = await CurrencyPair.get_or_none(pair=pair)
    if row.max_price is None or new_max_price > row.max_price:
        row.max_price = new_max_price
        return new_max_price
    return None
