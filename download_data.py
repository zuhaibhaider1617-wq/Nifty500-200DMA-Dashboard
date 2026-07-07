import pandas as pd
import yfinance as yf
import os
import time

print("=" * 50)
print("NIFTY 500 HISTORICAL DATA DOWNLOADER")
print("=" * 50)

# Read Nifty 500 list
stocks = pd.read_csv("data/ind_nifty500list.csv")

print(f"\nTotal Stocks Found: {len(stocks)}\n")

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

success = 0
failed = 0

for i, row in stocks.iterrows():

    symbol = row["Symbol"]
    yahoo_symbol = symbol + ".NS"

    print(f"[{i+1}/{len(stocks)}] Downloading {yahoo_symbol}")

    try:

        data = yf.download(
            yahoo_symbol,
            start="2020-01-01",
            end="2026-01-01",
            auto_adjust=True,
            progress=False,
            group_by="column"
        )

        # Remove MultiIndex if present
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if len(data) == 0:
            print("   ❌ No Data")
            failed += 1
            continue

        data.to_csv(f"data/{symbol}.csv")

        success += 1

        print(f"   ✅ {len(data)} rows")

    except Exception as e:

        failed += 1

        print(f"   ❌ Error : {e}")

    time.sleep(0.2)

print("\n" + "=" * 50)
print("DOWNLOAD COMPLETE")
print("=" * 50)

print("Successful :", success)
print("Failed     :", failed)