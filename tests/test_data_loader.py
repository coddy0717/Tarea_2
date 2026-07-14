import pytest

from report_automation.data_loader import load_transactions
from report_automation.exceptions import DataLoadError

VALID_CSV = """date,category,product,quantity,unit_price
2025-01-05,Electrónica,Laptop,2,850.00
2025-01-08,Electrónica,Mouse,10,15.50
"""


def write_csv(tmp_path, content, name="transactions.csv"):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def test_load_transactions_parses_valid_rows(tmp_path):
    csv_path = write_csv(tmp_path, VALID_CSV)

    transactions, errors = load_transactions(csv_path)

    assert errors == []
    assert len(transactions) == 2
    assert transactions[0]["product"] == "Laptop"
    assert transactions[0]["total"] == pytest.approx(1700.0)
    assert transactions[0]["date"].isoformat() == "2025-01-05"


def test_load_transactions_missing_file_raises(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(DataLoadError):
        load_transactions(missing_path)


def test_load_transactions_missing_columns_raises(tmp_path):
    csv_path = write_csv(tmp_path, "date,category,product\n2025-01-01,Oficina,Papel\n")

    with pytest.raises(DataLoadError):
        load_transactions(csv_path)


def test_load_transactions_empty_file_raises(tmp_path):
    csv_path = write_csv(tmp_path, "")

    with pytest.raises(DataLoadError):
        load_transactions(csv_path)


def test_load_transactions_skips_malformed_rows_and_reports_errors(tmp_path):
    content = (
        "date,category,product,quantity,unit_price\n"
        "2025-01-05,Electrónica,Laptop,2,850.00\n"
        "not-a-date,Electrónica,Mouse,10,15.50\n"
        "2025-01-09,Oficina,Papel,-3,4.25\n"
        "2025-01-10,Oficina,Papel,5,not-a-price\n"
    )
    csv_path = write_csv(tmp_path, content)

    transactions, errors = load_transactions(csv_path)

    assert len(transactions) == 1
    assert len(errors) == 3
    line_numbers = [line for line, _ in errors]
    assert line_numbers == [3, 4, 5]


def test_load_transactions_rejects_empty_category_or_product(tmp_path):
    content = (
        "date,category,product,quantity,unit_price\n"
        "2025-01-05,,Laptop,2,850.00\n"
    )
    csv_path = write_csv(tmp_path, content)

    transactions, errors = load_transactions(csv_path)

    assert transactions == []
    assert len(errors) == 1
