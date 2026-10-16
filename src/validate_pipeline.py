
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT = ROOT / "data" / "processed" / "transactions_classified.csv"


def main():
    print("Loading source and classified data...")

    source = pd.read_excel(SOURCE, engine="openpyxl")
    result = pd.read_csv(OUTPUT, low_memory=False)

    checks = {
        "Source and output row counts match":
            len(source) == len(result),

        "Duplicate flags match expected count":
            int(result["IsExcessExactDuplicate"].sum()) == 5268,

        "Cancellation flags match expected count":
            int(result["IsCancellationInvoice"].sum()) == 9288,

        "No negative positive-sales values":
            (result["PositiveSalesValue"] >= 0).all(),

        "Ineligible rows contribute zero positive sales":
            (
                result.loc[
                    ~result["EligiblePositiveSales"],
                    "PositiveSalesValue"
                ] == 0
            ).all(),

        "Duplicate rows are excluded from positive sales":
            (
                result.loc[
                    result["IsExcessExactDuplicate"],
                    "PositiveSalesValue"
                ] == 0
            ).all(),
    }

    print("\nVALIDATION RESULTS")
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {name}")

    print(f"\nSource rows: {len(source):,}")
    print(f"Output rows: {len(result):,}")
    print(
        "Eligible positive-sales rows: "
        f"{int(result['EligiblePositiveSales'].sum()):,}"
    )
    print(
        "Positive-sales value: "
        f"{result['PositiveSalesValue'].sum():,.2f}"
    )

    if not all(checks.values()):
        raise SystemExit("\nValidation failed. Investigate before proceeding.")

    print("\nAll pipeline validation checks passed.")


if __name__ == "__main__":
    main()
