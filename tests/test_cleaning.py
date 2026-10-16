
import pandas as pd
import pytest

from src.cleaning import classify_transactions


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "InvoiceNo": [
            "1001", "1001", "1002", "C1003", "1004", "1005"
        ],
        "StockCode": [
            "A", "A", "B", "C", "D", "E"
        ],
        "Description": [
            "Product A", "Product A", "Product B",
            "Product C", "Product D", None
        ],
        "Quantity": [2, 2, 3, -1, 1, 1],
        "InvoiceDate": pd.to_datetime([
            "2011-01-01", "2011-01-01", "2011-01-02",
            "2011-01-03", "2011-01-04", "2011-01-05"
        ]),
        "UnitPrice": [10.0, 10.0, 5.0, 7.0, 0.0, -2.0],
        "CustomerID": [101, 101, 102, 103, None, 105],
        "Country": ["UK", "UK", "UK", "UK", "UK", "UK"],
    })


def test_row_count_is_preserved(sample_data):
    result = classify_transactions(sample_data)
    assert len(result) == len(sample_data)


def test_exact_duplicate_is_flagged(sample_data):
    result = classify_transactions(sample_data)
    assert result["IsExcessExactDuplicate"].sum() == 1



def test_positive_sales_value(sample_data):
    result = classify_transactions(sample_data)

    # The second identical line is flagged and excluded from sales.
    assert result["PositiveSalesValue"].tolist() == [
        20.0, 0.0, 15.0, 0.0, 0.0, 0.0
    ]

    assert result["PositiveSalesValue"].sum() == 35.0



def test_cancellation_is_not_eligible_for_sales(sample_data):
    result = classify_transactions(sample_data)
    cancellation = result["InvoiceNo"].astype(str).str.startswith("C")

    assert result.loc[
        cancellation, "EligiblePositiveSales"
    ].eq(False).all()


def test_negative_quantity_is_flagged(sample_data):
    result = classify_transactions(sample_data)
    assert result["IsNegativeQuantity"].sum() == 1


def test_zero_and_negative_prices_are_flagged(sample_data):
    result = classify_transactions(sample_data)

    assert result["IsZeroPrice"].sum() == 1
    assert result["IsNegativePrice"].sum() == 1


def test_missing_customer_is_flagged(sample_data):
    result = classify_transactions(sample_data)
    assert result["HasMissingCustomerID"].sum() == 1


def test_required_columns_are_validated(sample_data):
    invalid = sample_data.drop(columns=["InvoiceNo"])

    with pytest.raises(ValueError, match="Missing required columns"):
        classify_transactions(invalid)
