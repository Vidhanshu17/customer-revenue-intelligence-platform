
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT = ROOT / "reports" / "record_investigation"

def main():
    df = pd.read_excel(SOURCE, engine="openpyxl")
    OUTPUT.mkdir(parents=True, exist_ok=True)

    invoice = df["InvoiceNo"].astype("string").str.strip()

    cases = {
        "exact_duplicates": df.loc[
            df.duplicated(keep=False)
        ],
        "negative_quantities": df.loc[
            df["Quantity"] < 0
        ],
        "zero_prices": df.loc[
            df["UnitPrice"] == 0
        ],
        "negative_prices": df.loc[
            df["UnitPrice"] < 0
        ],
        "cancellation_rows": df.loc[
            invoice.str.upper().str.startswith("C", na=False)
        ],
        "missing_customer_ids": df.loc[
            df["CustomerID"].isna()
        ],
    }

    for name, records in cases.items():
        path = OUTPUT / f"{name}.csv"
        records.to_csv(path, index=False)
        print(f"{name}: {len(records):,} rows -> {path}")

    print("\nInvestigation exports created.")
    print("The original dataset was not modified.")

if __name__ == "__main__":
    main()
