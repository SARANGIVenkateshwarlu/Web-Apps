from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

from app.config import settings
from app.core.data import fetch_api_ohlcv, load_csv_ohlcv
from app.core.ta import add_emas
from app.charts.lightweight import build_lightweight_chart

app = FastAPI(title="TradingView Super Chart API")


def get_df(symbol: str, timeframe: str):
    if settings.data_source == "csv":
        df = load_csv_ohlcv(settings.csv_path)
    else:
        df = fetch_api_ohlcv(symbol=symbol, timeframe=timeframe)  # uses API key
    return add_emas(df)


@app.get("/api/ohlcv")
def api_ohlcv(
    symbol: str = Query(settings.default_symbol),
    timeframe: str = Query(settings.default_timeframe),
):
    df = get_df(symbol, timeframe)
    return JSONResponse(df.to_dict(orient="records"))


@app.get("/chart", response_class=HTMLResponse)
def chart_page(
    symbol: str = Query(settings.default_symbol),
    timeframe: str = Query(settings.default_timeframe),
    ema_10: bool = True,
    ema_21: bool = True,
    ema_50: bool = True,
    ema_150: bool = True,
):
    df = get_df(symbol, timeframe)
    emas_enabled = []
    if ema_10:
        emas_enabled.append(10)
    if ema_21:
        emas_enabled.append(21)
    if ema_50:
        emas_enabled.append(50)
    if ema_150:
        emas_enabled.append(150)

    chart = build_lightweight_chart(df, emas_enabled=emas_enabled)
    html = chart.render(template="simple")  # returns HTML string with embedded JS
    return HTMLResponse(content=html)
