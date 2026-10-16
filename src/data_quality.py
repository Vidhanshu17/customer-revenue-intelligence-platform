
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_FILE = REPORT_DIR / "initial_data_profile.txt"

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


def inspect_dataset(file_path: Path) -> str:
    """Inspect the source dataset without changing the original file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}\n"
            "Place Online Retail.xlsx inside data/raw/."
        )

    print("Loading the original dataset...")
    df = pd.read_excel(file_path, engine="openpyxl")

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Required columns missing from dataset: "
            f"{sorted(missing_columns)}"
        )

    lines = []
    lines.append("CUSTOMER REVENUE INTELLIGENCE PLATFORM")
    lines.append("INITIAL DATA PROFILE")
    lines.append("=" * 60)

    lines.append(f"\nDataset file: {file_path.name}")
    lines.append(f"Rows: {len(df):,}")
    lines.append(f"Columns: {len(df.columns)}")
    lines.append(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    lines.append("\nCOLUMN NAMES AND DATA TYPES")
    lines.append(str(df.dtypes))

    lines.append("\nMISSING VALUES")
    lines.append(str(df.isna().sum()))

    lines.append("\nEXACT DUPLICATE ROWS")
    lines.append(str(df.duplicated().sum()))

    lines.append("\nDISTINCT VALUES")
    lines.append(f"Distinct invoices: {df['InvoiceNo'].nunique()}")
    lines.append(f"Distinct products: {df['StockCode'].nunique()}")
    lines.append(f"Distinct identified customers: {df['CustomerID'].nunique()}")
    lines.append(f"Distinct countries: {df['Country'].nunique()}")

    dates = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    lines.append("\nINVOICE DATE RANGE")
    lines.append(f"Earliest: {dates.min()}")
    lines.append(f"Latest: {dates.max()}")
    lines.append(f"Invalid dates: {dates.isna().sum()}")

    lines.append("\nQUANTITY PROFILE")
    lines.append(str(df["Quantity"].describe()))
    lines.append(f"Negative quantities: {(df['Quantity'] < 0).sum()}")
    lines.append(f"Zero quantities: {(df['Quantity'] == 0).sum()}")

    lines.append("\nUNIT PRICE PROFILE")
    lines.append(str(df["UnitPrice"].describe()))
    lines.append(f"Negative prices: {(df['UnitPrice'] < 0).sum()}")
    lines.append(f"Zero prices: {(df['UnitPrice'] == 0).sum()}")

    invoice_text = df["InvoiceNo"].astype("string").str.strip()
    cancellations = invoice_text.str.upper().str.startswith(
        "C", na=False
    )
    lines.append("\nCANCELLATION INDICATORS")
    lines.append(f"Rows with invoice numbers starting with C: {cancellations.sum()}")
    lines.append(
        "Distinct cancellation invoice IDs: "
        f"{df.loc[cancellations, 'InvoiceNo'].nunique()}"
    )

    lines.append("\nCUSTOMER ID COVERAGE")
    lines.append(f"Rows with missing CustomerID: {df['CustomerID'].isna().sum()}")
    lines.append(
        f"Rows with identified CustomerID: {df['CustomerID'].notna().sum()}"
    )

    lines.append("\nTOP 10 COUNTRIES BY ROW COUNT")
    lines.append(str(df["Country"].value_counts().head(10)))

    lines.append("\nSAMPLE RECORDS")
    lines.append(str(df.head(5).to_string(index=False)))

    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report = inspect_dataset(DATA_FILE)
    REPORT_FILE.write_text(report, encoding="utf-8")

    print("\nInspection completed.")
    print(f"Report saved to: {REPORT_FILE}")
    print("\nFirst part of the report:\n")
    print(report[:3500])


if __name__ == "__main__":
    main()
