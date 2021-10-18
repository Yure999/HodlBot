import pandas
import asyncio
from binance.client import Client
from binance import BinanceSocketManager
from binance import AsyncClient, DepthCacheManager, BinanceSocketManager

import credentials
import dbManager


class HodlBot:
    def __init__(self):
        self.client = AsyncClient(credentials.api_key, credentials.api_secret)
        self.socket_manager = BinanceSocketManager(self.client)
        self.socket = self.socket_manager.trade_socket("BTCUSDT")
        self.db_manager = dbManager.DbManager()

    def start_loading_information(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__fetch_data())

    async def __fetch_data(self):
        while True:
            await self.socket.__aenter__()
            response = await self.socket.recv()
            result = self.__map_response(response)
            self.db_manager.save_data(result)

    def __map_response(self, response):
        data = pandas.DataFrame([response])
        filtered_data = self.__filter_data(data)
        result = self.__format_results(filtered_data)
        return result

    def __filter_data(self, data):
        return data.loc[:, ["s", "E", "p"]]

    def __format_results(self, results):
        results.columns = ["Symbol", "Time", "Price"]
        results.Price = results.Price.astype(float)
        results.Time = pandas.to_datetime(results.Time, unit="ms")
        return results
