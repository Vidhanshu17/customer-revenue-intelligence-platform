
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_DIR = ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "transactions_classified.csv"
REPORT_FILE = ROOT / "reports" / "cleaning_summary.txt"

REQUIRED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]



def classify_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Classify source records and calculate provisional eligible sales."""

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = df.copy()
    result.columns = [column.strip() for column in result.columns]

    result["InvoiceDate"] = pd.to_datetime(
        result["InvoiceDate"], errors="coerce"
    )
    result["Quantity"] = pd.to_numeric(
        result["Quantity"], errors="coerce"
    )
    result["UnitPrice"] = pd.to_numeric(
        result["UnitPrice"], errors="coerce"
    )

    invoice = result["InvoiceNo"].astype("string").str.strip()

    result["IsCancellationInvoice"] = invoice.str.upper().str.startswith(
        "C", na=False
    )
    result["IsNegativeQuantity"] = result["Quantity"] < 0
    result["IsZeroPrice"] = result["UnitPrice"] == 0
    result["IsNegativePrice"] = result["UnitPrice"] < 0
    result["HasMissingCustomerID"] = result["CustomerID"].isna()
    result["HasMissingDescription"] = result["Description"].isna()

    # Keep the first occurrence and flag only excess exact copies.
    result["IsExcessExactDuplicate"] = result.duplicated(
        subset=REQUIRED_COLUMNS, keep="first"
    )

    # Original transaction-line value; retained for audit and investigation.
    result["LineValue"] = result["Quantity"] * result["UnitPrice"]

    # Provisional policy: regular sales must be positive-quantity,
    # positive-price, non-cancellation, non-duplicate records.
    result["EligiblePositiveSales"] = (
        (result["Quantity"] > 0)
        & (result["UnitPrice"] > 0)
        & ~result["IsCancellationInvoice"]
        & ~result["IsExcessExactDuplicate"]
    )

    result["PositiveSalesValue"] = result["LineValue"].where(
        result["EligiblePositiveSales"], 0.0
    )

    # Negative quantities are retained separately, not assumed to be
    # confirmed refunds.
    result["NegativeQuantityValue"] = result["LineValue"].where(
        result["IsNegativeQuantity"], 0.0
    )

    return result



def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source dataset not found: {SOURCE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Loading source dataset...")
    original = pd.read_excel(SOURCE, engine="openpyxl")

    classified = classify_transactions(original)

    # Save a separate output; never overwrite the source Excel file.
    classified.to_csv(OUTPUT_FILE, index=False)

    lines = [
        "CLEANING PIPELINE SUMMARY",
        "=" * 50,
        f"Source rows: {len(original):,}",
        f"Output rows: {len(classified):,}",
        f"Rows preserved: {len(original) == len(classified)}",
        f"Excess exact duplicates flagged: "
        f"{classified['IsExcessExactDuplicate'].sum():,}",
        f"Cancellation-marked rows: "
        f"{classified['IsCancellationInvoice'].sum():,}",
        f"Negative quantities: "
        f"{classified['IsNegativeQuantity'].sum():,}",
        f"Zero prices: {classified['IsZeroPrice'].sum():,}",
        f"Negative prices: {classified['IsNegativePrice'].sum():,}",
        f"Missing customer IDs: "
        f"{classified['HasMissingCustomerID'].sum():,}",
        f"Missing descriptions: "
        f"{classified['HasMissingDescription'].sum():,}",
        f"Eligible positive sales rows: "
        f"{classified['EligiblePositiveSales'].sum():,}",
        f"Eligible positive sales value: "
        f"{classified['PositiveSalesValue'].sum():,.2f}",
        "",
        "No source rows were deleted by this pipeline.",
        "Negative quantities and unusual prices remain flagged.",
        "Sales eligibility is a provisional analytical rule.",
    ]

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print(f"\nClassified data saved to: {OUTPUT_FILE}")
    print(f"Summary saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
