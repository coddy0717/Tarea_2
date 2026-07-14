"""Carga y validación de datos transaccionales desde archivos CSV."""

import csv
from datetime import datetime
from pathlib import Path

from .exceptions import DataLoadError

REQUIRED_COLUMNS = ("date", "category", "product", "quantity", "unit_price")


def load_transactions(csv_path):
    """Lee un archivo CSV de transacciones y lo convierte en una lista de dicts.

    Cada fila válida produce un diccionario con: date (date), category (str),
    product (str), quantity (int), unit_price (float) y total (float).

    Las filas con datos inválidos (fecha, cantidad o precio mal formados) se
    omiten y se reportan en la lista `errors`, en lugar de detener todo el
    proceso por un solo registro defectuoso.

    Retorna una tupla (transactions, errors).
    Lanza DataLoadError si el archivo no existe, está vacío o no contiene
    las columnas requeridas.
    """
    path = Path(csv_path)
    if not path.is_file():
        raise DataLoadError(f"No se encontró el archivo de datos: {csv_path}")

    try:
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise DataLoadError(f"El archivo está vacío: {csv_path}")

            missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
            if missing:
                raise DataLoadError(
                    f"Faltan columnas requeridas en el CSV: {', '.join(missing)}"
                )

            transactions = []
            errors = []
            for line_number, row in enumerate(reader, start=2):
                try:
                    transactions.append(_parse_row(row))
                except (ValueError, KeyError, AttributeError) as exc:
                    errors.append((line_number, str(exc)))
    except OSError as exc:
        raise DataLoadError(f"No se pudo leer el archivo {csv_path}: {exc}") from exc

    return transactions, errors


def _parse_row(row):
    date_value = datetime.strptime(row["date"].strip(), "%Y-%m-%d").date()
    category = row["category"].strip()
    product = row["product"].strip()
    if not category or not product:
        raise ValueError("category y product no pueden estar vacíos")

    quantity = int(row["quantity"])
    unit_price = float(row["unit_price"])
    if quantity <= 0 or unit_price < 0:
        raise ValueError("quantity debe ser > 0 y unit_price >= 0")

    return {
        "date": date_value,
        "category": category,
        "product": product,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": round(quantity * unit_price, 2),
    }
