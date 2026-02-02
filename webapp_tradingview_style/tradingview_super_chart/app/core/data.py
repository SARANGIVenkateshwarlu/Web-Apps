import os
from typing import Literal, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DATA_API_KEY", "")
API_BASE = os.getenv("DATA_API_BASE", "")

Timeframe = Literal["1m", "5m", "15m", "1h", "1d"]


def load_csv_ohlcv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Expect columns: time, open, high, low, close, volume
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    return df[["time", "open", "high", "low", "close", "volume"]]


def fetch_api_ohlcv(
    symbol: str,
    timeframe: Timeframe = "1h",
    limit: int = 500,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> pd.DataFrame:
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    params = {
        "symbol": symbol,
        "timeframe": timeframe,
        "limit": limit,
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end

    url = f"{API_BASE}/ohlcv"
    r = requests.get(url, headers=headers, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    # Example JSON -> DataFrame; adapt keys to your provider.
    df = pd.DataFrame(
        data,
        columns=["time", "open", "high", "low", "close", "volume"],
    )
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    return df
