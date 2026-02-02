import streamlit as st

from app.config import settings
from app.core.data import load_csv_ohlcv, fetch_api_ohlcv
from app.core.ta import add_emas
from app.charts.plotly_charts import build_plotly_super_chart

# Optionally: from lightweight_charts import StreamlitChart (if your wrapper exposes it)


def get_df(source: str, symbol: str, timeframe: str):
    if source == "CSV":
        df = load_csv_ohlcv(settings.csv_path)
    else:
        df = fetch_api_ohlcv(symbol=symbol, timeframe=timeframe)
    return add_emas(df)


def main():
    st.set_page_config(page_title="Super Volume Chart", layout="wide")

    st.sidebar.header("Data")
    source = st.sidebar.selectbox("Source", ["CSV", "API"])
    symbol = st.sidebar.text_input("Symbol", value=settings.default_symbol)
    timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "1d"])

    st.sidebar.header("Overlays")
    ema_10 = st.sidebar.checkbox("EMA 10", value=True)
    ema_21 = st.sidebar.checkbox("EMA 21", value=True)
    ema_50 = st.sidebar.checkbox("EMA 50", value=True)
    ema_150 = st.sidebar.checkbox("EMA 150", value=True)

    emas_enabled = [
        p
        for p, enabled in zip(
            [10, 21, 50, 150],
            [ema_10, ema_21, ema_50, ema_150],
        )
        if enabled
    ]

    df = get_df(source, symbol, timeframe)

    st.title("TradingView‑style Super Volume Chart")

    fig = build_plotly_super_chart(df, emas_enabled=emas_enabled)
    st.plotly_chart(fig, use_container_width=True)

    # Example: show data preview and allow custom CSV upload
    st.sidebar.header("Custom CSV")
    csv_file = st.sidebar.file_uploader("Upload OHLCV CSV", type=["csv"])
    if csv_file is not None:
        custom_df = load_csv_ohlcv(csv_file)
        custom_df = add_emas(custom_df)
        fig2 = build_plotly_super_chart(custom_df, emas_enabled=emas_enabled)
        st.subheader("Custom CSV Chart")
        st.plotly_chart(fig2, use_container_width=True)


if __name__ == "__main__":
    main()
