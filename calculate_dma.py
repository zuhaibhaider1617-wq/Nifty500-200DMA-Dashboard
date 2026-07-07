import pandas as pd

# -----------------------
# SETTINGS
# -----------------------

SYMBOL = "RELIANCE"
SELECTED_DATE = "2022-03-15"

# -----------------------
# LOAD DATA
# -----------------------

df = pd.read_csv(f"data/{SYMBOL}.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------
# CALCULATE 200 DMA
# -----------------------

df["200DMA"] = df["Close"].rolling(window=200).mean()

# -----------------------
# GET SELECTED DATE
# -----------------------

row = df[df["Date"] == SELECTED_DATE]

if len(row) == 0:
    print("Date not found!")

else:

    row = row.iloc[0]

    print("="*40)
    print("Stock :", SYMBOL)
    print("Date  :", SELECTED_DATE)
    print("="*40)

    print("Close Price :", round(row["Close"],2))
    print("200 DMA     :", round(row["200DMA"],2))

    if row["Close"] > row["200DMA"]:
        print("Status      : ABOVE 200 DMA")

    else:
        print("Status      : BELOW 200 DMA")

    diff = ((row["Close"]-row["200DMA"])/row["200DMA"])*100

    print("Difference  :", round(diff,2),"%")