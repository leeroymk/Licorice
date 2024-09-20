import logging
import os
import aiohttp
import asyncio
from decimal import Decimal


def get_pair_name(exchange, pair):
    base, quote = pair.split("/")

    format_rules = {
        "binance": f"{base}{quote}",
        "coinmarketcap": quote,
        "bybit": f"{base}{quote}",
        "gateio": f"{base}_{quote}",
        "kucoin": f"{base}-{quote}",
    }

    return format_rules.get(exchange, None)


async def get_price(session, url, params=None, headers=None):
    try:
        async with session.get(url, params=params, headers=headers) as response:
            data = await response.json()
            if response.status != 200:
                return None
            return data
    except Exception as e:
        logging.error(f"Error: {str(e)}, {type(e)}, {e.args}")
        return None


async def get_binance_price(session, pair):
    exchange = "binance"
    pair_name = get_pair_name(exchange, pair)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair_name}"
    data = await get_price(session, url)
    price = Decimal(data.get("price", 0)) if data else None
    return price, exchange


async def get_coinmarketcap_price(session, pair):
    exchange = "coinmarketcap"
    pair_name = get_pair_name(exchange, pair)
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {"convert": pair_name}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("CMC_API_KEY"),
    }
    data = await get_price(session, url, params=params, headers=headers)
    try:
        price = Decimal(data["data"][0]["quote"][pair_name]["price"]) if data else None
        return price, exchange
    except (KeyError, TypeError):
        return None, exchange


async def get_bybit_price(session, pair):
    exchange = "bybit"
    pair_name = get_pair_name(exchange, pair)
    url = "https://api.bybit.com/v5/market/tickers"
    params = {"category": "spot", "symbol": pair_name}
    data = await get_price(session, url, params=params)
    try:
        price = Decimal(data["result"]["list"][0]["lastPrice"]) if data else None
        return price, exchange
    except (KeyError, TypeError):
        return None, exchange


async def get_gateio_price(session, pair):
    exchange = "gateio"
    pair_name = get_pair_name(exchange, pair)
    url = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={pair_name}"
    data = await get_price(session, url)
    try:
        price = Decimal(data[0].get("last", 0)) if data else None
        return price, exchange
    except (KeyError, IndexError, TypeError):
        return None, exchange


async def get_kucoin_price(session, pair):
    exchange = "kucoin"
    pair_name = get_pair_name(exchange, pair)
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={pair_name}"
    data = await get_price(session, url)
    try:
        price = Decimal(data["data"].get("price", 0)) if data else None
        return price, exchange
    except (AttributeError, TypeError):
        return None, exchange


async def get_all_prices(pair):
    async with aiohttp.ClientSession() as session:
        results = {}

        results[pair] = []

        tasks = [
            get_binance_price(session, pair),
            get_coinmarketcap_price(session, pair),
            get_bybit_price(session, pair),
            get_gateio_price(session, pair),
            get_kucoin_price(session, pair),
        ]

        responses = await asyncio.gather(*tasks)

        filtered_responses = filter_responses(responses)

        max_price, exchange = max(filtered_responses, key=lambda x: x[0])
        min_price = min(filtered_responses, key=lambda x: x[0])[0]

        return min_price, max_price, exchange


def filter_responses(responses):
    filtered_prices = [(price, exchange) for price, exchange in responses if price is not None]

    if not filtered_prices:
        raise ValueError("Нет доступных цен для сравнения.")

    return filtered_prices
