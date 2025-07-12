import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

# 设置页面标题和布局
st.set_page_config(page_title="📈 多功能股票分析", layout="wide")

st.title("📊 多功能股票分析平台（Streamlit + yfinance）")

# --- 侧边栏输入 ---
st.sidebar.header("🔧 参数设置")

# 多股票输入
tickers_input = st.sidebar.text_input("输入股票代码（多个用逗号分隔）", value="AAPL, MSFT, TSLA")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# 时间范围选择
date_range_dict = {
    "1 周": 7,
    "1 月": 30,
    "6 个月": 182,
    "1 年": 365,
    "10 年": 3650
}
date_range_label = st.sidebar.selectbox("选择时间范围", list(date_range_dict.keys()), index=3)

# 频率选择
freq_dict = {
    "日线": "D",
    "周线": "W",
    "月线": "M",
    "年线": "Y"
}
freq_label = st.sidebar.selectbox("选择数据频率", list(freq_dict.keys()), index=0)
freq = freq_dict[freq_label]

# 是否显示移动平均线
show_ma = st.sidebar.checkbox("📉 显示移动平均线 (20, 50, 200)", value=True)

# 是否显示成交量图
show_volume = st.sidebar.checkbox("📊 显示成交量", value=True)

# --- 主区展示 ---
end_date = datetime.today()
start_date = end_date - timedelta(days=date_range_dict[date_range_label])

for ticker in tickers:
    st.subheader(f"📌 股票代码：{ticker}")

    try:
        df = yf.download(ticker, start=start_date, end=end_date)

        # 判断数据是否为空 + 是否包含所需列
        if df.empty or not {"Close", "Volume"}.issubset(df.columns):
            st.warning(f"⚠️ 无法获取 {ticker} 的有效股票数据，或缺少 Close/Volume 列。")
            continue
        
        df.index = pd.to_datetime(df.index)
        df = df[["Close", "Volume"]]
        df_resampled = df.resample(freq).agg({"Close": "last", "Volume": "sum"})

        # 计算移动平均线
        if show_ma:
            df_resampled["MA20"] = df_resampled["Close"].rolling(window=20).mean()
            df_resampled["MA50"] = df_resampled["Close"].rolling(window=50).mean()
            df_resampled["MA200"] = df_resampled["Close"].rolling(window=200).mean()

        # 绘图
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_resampled.index, df_resampled["Close"], label="Close", linewidth=2)

        if show_ma:
            ax.plot(df_resampled.index, df_resampled["MA20"], label="MA20", linestyle="--")
            ax.plot(df_resampled.index, df_resampled["MA50"], label="MA50", linestyle="--")
            ax.plot(df_resampled.index, df_resampled["MA200"], label="MA200", linestyle="--")

        ax.set_title(f"{ticker} 收盘价与均线 - {date_range_label} ({freq_label})", fontsize=14)
        ax.set_xlabel("日期")
        ax.set_ylabel("价格（USD）")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # 成交量图
        if show_volume:
            fig2, ax2 = plt.subplots(figsize=(10, 2))
            ax2.bar(df_resampled.index, df_resampled["Volume"], color="orange", alpha=0.6)
            ax2.set_title(f"{ticker} 成交量", fontsize=12)
            ax2.set_xlabel("日期")
            ax2.set_ylabel("成交量")
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ 错误：无法获取 {ticker} 数据。错误信息：{e}")

# --- 财经新闻推荐展示 ---
st.markdown("---")
st.subheader("📰 财经新闻推荐（示例）")

news_list = [
    {"title": "苹果公司发布最新季度财报", "url": "https://finance.yahoo.com/quote/AAPL"},
    {"title": "特斯拉宣布超级工厂扩建计划", "url": "https://finance.yahoo.com/quote/TSLA"},
    {"title": "微软与OpenAI深化合作", "url": "https://finance.yahoo.com/quote/MSFT"},
]

for news in news_list:
    st.markdown(f"- [{news['title']}]({news['url']})")
