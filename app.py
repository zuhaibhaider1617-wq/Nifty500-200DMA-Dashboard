import streamlit as st
import pandas as pd
from datetime import date

from generate_report import generate_report

stocks = pd.read_csv("data/ind_nifty500list.csv")

st.set_page_config(
    page_title="Nifty 500 Historical 200 DMA Dashboard",
    layout="wide"
)

st.title("📈 Nifty 500 Historical 200 DMA Dashboard")

st.write("Analyze Nifty 500 stocks based on their 200-Day Moving Average.")

# -----------------------
# DATE PICKER
# -----------------------

selected_date = st.date_input(
    "📅 Select Date",
    value=date(2022,3,15),
    min_value=date(2020,1,1),
    max_value=date(2025,12,31)
)

st.write("Selected Date:", selected_date)

# -----------------------
# SEARCH BOX
# -----------------------


# -----------------------
# INDUSTRY FILTER
# -----------------------

industry = st.selectbox(
    "🏭 Select Industry",
    [
        "All",
        "Financial Services",
        "Information Technology",
        "Power",
        "Capital Goods",
        "Healthcare",
        "Fast Moving Consumer Goods"
    ]
)

status = st.selectbox(
    "📈 Status",
    [
        "All",
        "Above",
        "Below"
    ]
)

stock_options = ["None"] + sorted(
    (
        stocks["Symbol"] + " - " + stocks["Company Name"]
    ).tolist()
)

stock = st.selectbox(
    "📊 Search & Select Stock",
    stock_options
)


# -----------------------
# GENERATE REPORT BUTTON
# -----------------------

if st.button("Generate Report"):

    with st.spinner("Generating report..."):
        report = generate_report(str(selected_date))
        if report.empty:
            st.warning("No stocks found for the selected filters/date.")
            st.stop()


    # -----------------------
    # INDUSTRY FILTER
    # -----------------------

    if industry != "All":
        report = report[
            report["Industry"] == industry
        ]

    # -----------------------
    # STATUS FILTER
    # -----------------------

    if status != "All":
        report = report[
            report["Status"] == status
        ]

    # -----------------------
    # STOCK FILTER
    # -----------------------

    if stock != "None":

        selected_symbol = stock.split(" - ")[0]

        report = report[
            report["Symbol"] == selected_symbol
        ]

    # -----------------------
    # CALCULATE SUMMARY
    # -----------------------

    total = len(report)
    above = (report["Status"] == "Above").sum()
    below = (report["Status"] == "Below").sum()
    breadth = round((above / total) * 100, 2) if total > 0 else 0

    st.success(f"Showing report for {selected_date}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📊 Processed Stocks", total)
    col2.metric("🟢 Above 200 DMA", above)
    col3.metric("🔴 Below 200 DMA", below)
    col4.metric("📈 Market Breadth", f"{breadth}%")

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )