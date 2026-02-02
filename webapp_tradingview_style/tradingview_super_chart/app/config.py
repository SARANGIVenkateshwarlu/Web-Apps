from pydantic import BaseSettings


class Settings(BaseSettings):
    data_source: str = "csv"        # csv or api
    csv_path: str = "data/sample_ohlcv.csv"
    default_symbol: str = "BTCUSDT"
    default_timeframe: str = "1h"

    class Config:
        env_file = ".env"


settings = Settings()
