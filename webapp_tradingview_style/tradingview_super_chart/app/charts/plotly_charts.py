from typing import List

import pandas as pd
import plotly.graph_objects as go

from app.core.ta import EMA_PERIODS


def build_plotly_super_chart(
    df: pd.DataFrame,
    emas_enabled: List[int] | None = None,
) -> go.Figure:
    emas_enabled = emas_enabled or EMA_PERIODS

    fig = go.Figure()

    # Candlesticks
    fig.add_trace(
        go.Candlestick(
            x=df["time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price",
        )
    )

    # EMAs
    for p in EMA_PERIODS:
        if p not in emas_enabled:
            continue
        ema_col = f"ema_{p}"
        if ema_col not in df.columns:
            continue
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df[ema_col],
                mode="lines",
                name=f"EMA {p}",
            )
        )

    # Volume bars on secondary axis
    fig.add_trace(
        go.Bar(
            x=df["time"],
            y=df["volume"],
            name="Volume",
            marker_color="rgba(150,150,150,0.4)",
            yaxis="y2",
        )
    )

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        yaxis=dict(title="Price"),
        yaxis2=dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig
