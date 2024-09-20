import logging
from aiohttp import web
from app.db.models import CurrencyPair
from app.utils import setup_logging


setup_logging()


async def create_currency_pair(request):
    data = await request.json()
    currency_pair = await CurrencyPair.create(
        pair=data["pair"],
        exchange=data["exchange"],
        price=data.get("price"),
        min_price=data.get("min_price"),
        max_price=data.get("max_price"),
    )
    return web.json_response(
        {
            "id": currency_pair.id,
            "pair": currency_pair.pair,
            "exchange": currency_pair.exchange,
            "price": str(currency_pair.price),
            "min_price": str(currency_pair.min_price),
            "max_price": str(currency_pair.max_price),
            "date": currency_pair.date.isoformat(),
        }
    )


async def get_currency_pair(request):
    try:
        pair_id = int(request.match_info["pair_id"])
        currency_pair = await CurrencyPair.get(id=pair_id)
        if not currency_pair:
            return web.json_response({"error": "Currency pair not found"}, status=404)

        return web.json_response(
            {
                "id": currency_pair.id,
                "pair": currency_pair.pair,
                "exchange": currency_pair.exchange,
                "price": str(currency_pair.price),
                "min_price": str(currency_pair.min_price),
                "max_price": str(currency_pair.max_price),
                "date": currency_pair.date.isoformat(),
            }
        )
    except Exception as e:
        logging.error(f"Error in get_currency_pair: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def get_all_currency_pairs(request):
    currency_pairs = await CurrencyPair.all()
    result = [
        {
            "id": pair.id,
            "pair": pair.pair,
            "exchange": pair.exchange,
            "price": str(pair.price),
            "min_price": str(pair.min_price),
            "max_price": str(pair.max_price),
            "date": pair.date.isoformat(),
        }
        for pair in currency_pairs
    ]
    return web.json_response(result)


async def update_currency_pair(request):
    pair_id = int(request.match_info["pair_id"])
    data = await request.json()
    currency_pair = await CurrencyPair.get(id=pair_id)
    if not currency_pair:
        return web.json_response({"error": "Currency pair not found"}, status=404)

    currency_pair.pair = data.get("pair", currency_pair.pair)
    currency_pair.exchange = data.get("exchange", currency_pair.exchange)
    currency_pair.price = data.get("price", currency_pair.price)
    currency_pair.min_price = data.get("min_price", currency_pair.min_price)
    currency_pair.max_price = data.get("max_price", currency_pair.max_price)

    await currency_pair.save()

    return web.json_response(
        {
            "id": currency_pair.id,
            "pair": currency_pair.pair,
            "exchange": currency_pair.exchange,
            "price": str(currency_pair.price),
            "min_price": str(currency_pair.min_price),
            "max_price": str(currency_pair.max_price),
            "date": currency_pair.date.isoformat(),
        }
    )


async def delete_currency_pair(request):
    pair_id = int(request.match_info["pair_id"])
    currency_pair = await CurrencyPair.get(id=pair_id)
    if not currency_pair:
        return web.json_response({"error": "Currency pair not found"}, status=404)

    await currency_pair.delete()
    return web.json_response({"status": "deleted"})
