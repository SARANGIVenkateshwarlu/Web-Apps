import pandas as pd

EMA_PERIODS = [10, 21, 50, 150]


def add_emas(df: pd.DataFrame, periods=EMA_PERIODS) -> pd.DataFrame:
    out = df.copy()
    for p in periods:
        out[f"ema_{p}"] = out["close"].ewm(span=p, adjust=False).mean()
    return out
