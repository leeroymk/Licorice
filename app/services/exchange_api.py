import logging
import os
import aiohttp
import asyncio

from app.utils.logging_setup import setup_logging


setup_logging()


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


async def fetch_price(session, url, params=None, headers=None):
    try:
        async with session.get(url, params=params, headers=headers) as response:
            data = await response.json()
            if response.status != 200:
                return {"error": f"Error: {data.get('message', 'Unknown error')}"}
            return data
    except Exception as e:
        logging.error(f"Error: {str(e)}, {type(e)}, {e.args}")
        return {"error": f"{str(e)}"}


async def fetch_binance_price(session, pair):
    pair_name = get_pair_name("binance", pair)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair_name}"
    data = await fetch_price(session, url)
    return {"price": data.get("price", data.get("error"))}


async def fetch_coinmarketcap_price(session, pair):
    pair_name = get_pair_name("coinmarketcap", pair)
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {"convert": pair_name}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("CMC_API_KEY"),
    }
    data = await fetch_price(session, url, params=params, headers=headers)
    try:
        return {"price": data["data"][0]["quote"][pair_name]["price"]}
    except KeyError:
        return {"error": data.get("error", "Unable to fetch data")}


async def fetch_bybit_price(session, pair):
    pair_name = get_pair_name("bybit", pair)
    url = "https://api.bybit.com/v5/market/tickers"
    params = {"category": "spot", "symbol": pair_name}
    data = await fetch_price(session, url, params=params)
    try:
        return {"price": data["result"]["list"][0]["lastPrice"]}
    except KeyError:
        return {"error": data.get("error", "Unable to fetch data")}


async def fetch_gateio_price(session, pair):
    pair_name = get_pair_name("gateio", pair)
    url = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={pair_name}"
    data = await fetch_price(session, url)
    try:
        return {"price": data[0].get("last")}
    except (KeyError, IndexError):
        return {"error": data.get("message", "Unable to fetch data")}


async def fetch_kucoin_price(session, pair):
    pair_name = get_pair_name("kucoin", pair)
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={pair_name}"
    data = await fetch_price(session, url)
    try:
        return {"price": data["data"].get("price")}
    except AttributeError:
        return {"error": "Unable to fetch data"}


def organize_results(pairs, results):
    organized_results = {}
    for i, pair in enumerate(pairs):
        organized_results[pair] = {
            "binance": results[i * 5].get("price", "Error"),
            "coinmarket": results[i * 5 + 1].get("price", "Error"),
            "bybit": results[i * 5 + 2].get("price", "Error"),
            "gateio": results[i * 5 + 3].get("price", "Error"),
            "kucoin": results[i * 5 + 4].get("price", "Error"),
        }
    return organized_results


async def fetch_all_prices_for_pairs(pairs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for pair in pairs:
            tasks.append(fetch_binance_price(session, pair))
            tasks.append(fetch_coinmarketcap_price(session, pair))
            tasks.append(fetch_bybit_price(session, pair))
            tasks.append(fetch_gateio_price(session, pair))
            tasks.append(fetch_kucoin_price(session, pair))

        results = await asyncio.gather(*tasks)
        return organize_results(pairs, results)


pairs = ["BTC/USDT", "BTC/ETH", "BTC/XMR", "BTC/SOL", "BTC/RUB", "BTC/DOGE"]
results = asyncio.run(fetch_all_prices_for_pairs(pairs))
logging.info(results)
