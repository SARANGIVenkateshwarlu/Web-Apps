from typing import List

import pandas as pd
from lightweight_charts import Chart

from app.core.ta import EMA_PERIODS


def build_lightweight_chart(
    df: pd.DataFrame,
    emas_enabled: List[int] | None = None,
    volume: bool = True,
    toolbox: bool = True,
) -> Chart:
    emas_enabled = emas_enabled or EMA_PERIODS

    chart = Chart(
        width=1200,
        height=700,
        title="Super Volume Chart",
        toolbox=toolbox,       # toolbar with zoom/pan, screenshot, etc.
    )

    # Main candlestick series
    candle = chart.add_candlestick_series()
    candle.set(df[["time", "open", "high", "low", "close"]])

    # Volume series
    if volume:
        vol = chart.add_histogram_series(
            price_format={"type": "volume"},
            price_scale_id="volume",
            overlay=True,
        )
        vol.set(df[["time", "volume"]])

    # EMAs as overlay lines
    for p in EMA_PERIODS:
        if p not in emas_enabled:
            continue
        ema_col = f"ema_{p}"
        if ema_col not in df.columns:
            continue
        ema_series = chart.add_line_series(
            line_width=2,
            title=f"EMA {p}",
        )
        ema_data = df[["time", ema_col]].rename(columns={ema_col: "value"})
        ema_series.set(ema_data)

    # Enable crosshair + interaction
    chart.crosshair(mode="normal")
    chart.legend(visible=True)
    chart.time_scale(border_visible=True)

    return chart
