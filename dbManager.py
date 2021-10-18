import sqlalchemy


class DbManager:
    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///BTCUSDTstream.db")

    def save_data(self, data):
        data.to_sql("BTCUSDT", self.engine, if_exists="append", index=False)
        print(data)
