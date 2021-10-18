import sqlalchemy
import pandas


class DbManager:
    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///BTCUSDTstream.db")

    def save_data(self, data):
        data.to_sql("BTCUSDT", self.engine, if_exists="append", index=False)


    def read_btc_data(self):
        data = pandas.read_sql("BTCUSDT", self.engine)
        print(data)