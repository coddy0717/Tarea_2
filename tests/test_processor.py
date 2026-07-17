import datetime

import pytest

from report_automation.processor import (
    calculate_summary,
    group_by_category,
    monthly_trend,
    top_products,
)


def make_tx(date, category, product, quantity, unit_price):
    return {
        "date": datetime.date.fromisoformat(date),
        "category": category,
        "product": product,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": round(quantity * unit_price, 2),
    }


TRANSACTIONS = [
    make_tx("2025-01-05", "Electrónica", "Laptop", 2, 850.0),
    make_tx("2025-01-08", "Electrónica", "Mouse", 10, 15.5),
    make_tx("2025-02-02", "Electrónica", "Laptop", 1, 850.0),
    make_tx("2025-02-10", "Oficina", "Papel", 15, 4.25),
]


def test_calculate_summary_with_data():
    summary = calculate_summary(TRANSACTIONS)

    assert summary["total_transactions"] == 4
    assert summary["unique_products"] == 3
    assert summary["total_revenue"] == pytest.approx(2768.75)
    assert summary["average_ticket"] == pytest.approx(692.19, abs=0.01)


def test_calculate_summary_empty_list():
    summary = calculate_summary([])

    assert summary == {
        "total_revenue": 0.0,
        "total_transactions": 0,
        "average_ticket": 0.0,
        "unique_products": 0,
    }


def test_group_by_category_sorted_by_revenue_desc():
    result = group_by_category(TRANSACTIONS)

    assert result[0]["category"] == "Electrónica"
    assert result[0]["count"] == 3
    assert result[0]["revenue"] == pytest.approx(1700.0 + 155.0 + 850.0)
    assert result[1]["category"] == "Oficina"
    assert result[1]["revenue"] == pytest.approx(63.75)


def test_top_products_orders_and_limits():
    result = top_products(TRANSACTIONS, limit=2)

    assert len(result) == 2
    assert result[0]["product"] == "Laptop"
    assert result[0]["revenue"] == pytest.approx(2550.0)
    assert result[1]["product"] == "Mouse"


def test_top_products_invalid_limit_raises():
    with pytest.raises(ValueError):
        top_products(TRANSACTIONS, limit=0)


def test_monthly_trend_groups_chronologically():
    result = monthly_trend(TRANSACTIONS)

    assert [item["month"] for item in result] == ["2025-01", "2025-02"]
    assert result[0]["revenue"] == pytest.approx(1855.0)
    assert result[1]["revenue"] == pytest.approx(913.75)
