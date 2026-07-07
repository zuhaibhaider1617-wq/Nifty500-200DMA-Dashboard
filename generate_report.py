import pandas as pd
import os

def generate_report(selected_date):

    # =====================
    # SETTINGS
    # =====================

    SELECTED_DATE = pd.to_datetime(selected_date)

    # =====================
    # LOAD NIFTY LIST
    # =====================

    stocks = pd.read_csv("data/ind_nifty500list.csv")

    results = []

    print("Generating Report...\n")

    # =====================
    # LOOP THROUGH STOCKS
    # =====================

    for _, stock in stocks.iterrows():

        symbol = stock["Symbol"]
        company = stock["Company Name"]

        file_path = f"data/{symbol}.csv"

        if not os.path.exists(file_path):
            continue

        try:

            df = pd.read_csv(file_path)

            df["Date"] = pd.to_datetime(df["Date"])

            df["200DMA"] = df["Close"].rolling(200).mean()

            row = df[df["Date"] == SELECTED_DATE]

            if len(row) == 0:
                continue

            row = row.iloc[0]

            close = row["Close"]
            dma = row["200DMA"]

            if pd.isna(dma):
                continue

            status = "Above" if close > dma else "Below"

            diff = ((close - dma) / dma) * 100

            results.append({
                "Symbol": symbol,
                "Company": company,
                "Industry": stock["Industry"],
                "Close": round(close,2),
                "200DMA": round(dma,2),
                "Status": status,
                "Difference %": round(diff,2)
    })

        except Exception as e:
            print(f"Error in {symbol}: {e}")

    # =====================
    # SAVE REPORT
    # =====================

    report = pd.DataFrame(results)

    print("Rows:", len(report))
    print("Columns:", report.columns.tolist())

    if report.empty:
        print("REPORT IS EMPTY!")
        return report

    report = report.sort_values(
        by="Difference %",
        ascending=False
    )

    report.to_csv("output/report.csv", index=False)
    report.to_excel("output/report.xlsx", index=False)
    return report

