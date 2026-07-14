"""Cálculo de indicadores (KPIs) a partir de transacciones ya cargadas.

Funcionalidad a cargo del Equipo A: agregación y ranking de datos de venta.
"""

from collections import defaultdict


def calculate_summary(transactions):
    """Calcula los indicadores globales de un conjunto de transacciones.

    Retorna un dict con: total_revenue, total_transactions,
    average_ticket y unique_products. Si la lista está vacía, retorna
    todos los indicadores en cero en lugar de fallar por división entre 0.
    """
    if not transactions:
        return {
            "total_revenue": 0.0,
            "total_transactions": 0,
            "average_ticket": 0.0,
            "unique_products": 0,
        }

    total_revenue = round(sum(t["total"] for t in transactions), 2)
    total_transactions = len(transactions)
    unique_products = len({t["product"] for t in transactions})
    average_ticket = round(total_revenue / total_transactions, 2)

    return {
        "total_revenue": total_revenue,
        "total_transactions": total_transactions,
        "average_ticket": average_ticket,
        "unique_products": unique_products,
    }


def group_by_category(transactions):
    """Agrupa el ingreso y número de ventas por categoría.

    Algoritmo: recorre las transacciones una sola vez acumulando ingreso y
    conteo en un diccionario indexado por categoría (O(n)); al final ordena
    las categorías de mayor a menor ingreso para facilitar su presentación.
    """
    totals = defaultdict(lambda: {"revenue": 0.0, "count": 0})
    for t in transactions:
        entry = totals[t["category"]]
        entry["revenue"] += t["total"]
        entry["count"] += 1

    result = [
        {"category": category, "revenue": round(data["revenue"], 2), "count": data["count"]}
        for category, data in totals.items()
    ]
    result.sort(key=lambda item: item["revenue"], reverse=True)
    return result


def top_products(transactions, limit=5):
    """Retorna los `limit` productos con mayor ingreso acumulado.

    Algoritmo: agrupa por nombre de producto sumando el campo `total` de
    cada transacción y ordena de mayor a menor ingreso (sort estable, por
    lo que los empates conservan el orden de aparición original).
    """
    if limit <= 0:
        raise ValueError("limit debe ser mayor que cero")

    totals = defaultdict(float)
    for t in transactions:
        totals[t["product"]] += t["total"]

    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return [
        {"product": name, "revenue": round(revenue, 2)}
        for name, revenue in ranked[:limit]
    ]


def monthly_trend(transactions):
    """Calcula el ingreso total agrupado por mes (formato YYYY-MM).

    Retorna una lista de dicts (month, revenue) ordenada cronológicamente,
    útil para graficar la tendencia de ventas en el tiempo.
    """
    totals = defaultdict(float)
    for t in transactions:
        month_key = t["date"].strftime("%Y-%m")
        totals[month_key] += t["total"]

    return [
        {"month": month, "revenue": round(revenue, 2)}
        for month, revenue in sorted(totals.items())
    ]
