import pandas
# import sqlalchemy
import json
import asyncio
from binance.client import Client
from binance import BinanceSocketManager
from binance import AsyncClient, DepthCacheManager, BinanceSocketManager

import credentials

client = Client(credentials.api_key, credentials.api_secret)
socket_manager = BinanceSocketManager(client)
socket = socket_manager.trade_socket("BTCUSDT")


async def fetch_data():
    await socket.__aenter__()
    response = await socket.recv()
    print(map_response(response))


def map_response(response):
    data = pandas.DataFrame([response])
    filtered_data = data.loc[:, ["s", "E", "p"]]
    filtered_data.columns = ["Symbol", "Time", "Price"]
    filtered_data.Price = filtered_data.Price.astype(float)
    filtered_data.Time = pandas.to_datetime(filtered_data.Time, unit="ms")
    return filtered_data

loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_data())
