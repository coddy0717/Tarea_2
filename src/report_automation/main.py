"""Punto de entrada de la aplicación de automatización de reportes."""

import argparse
import sys
from pathlib import Path

from .data_loader import load_transactions
from .exceptions import ReportAutomationError
from .processor import calculate_summary, group_by_category, top_products
from .report_generator import generate_excel_report, generate_html_report


def run(input_csv, output_dir):
    """Ejecuta el flujo completo: cargar datos, calcular KPIs y generar reportes."""
    transactions, errors = load_transactions(input_csv)

    for line_number, message in errors:
        print(f"[AVISO] Fila {line_number} omitida: {message}", file=sys.stderr)

    summary = calculate_summary(transactions)
    categories = group_by_category(transactions)
    products = top_products(transactions)

    output_dir = Path(output_dir)
    excel_path = generate_excel_report(
        summary, categories, products, output_dir / "reporte_ventas.xlsx"
    )
    html_path = generate_html_report(
        summary, categories, products, output_dir / "reporte_ventas.html"
    )

    return {
        "summary": summary,
        "excel_path": excel_path,
        "html_path": html_path,
        "skipped_rows": len(errors),
    }


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Automatización de reportes e informes de ventas."
    )
    parser.add_argument("--input", required=True, help="Ruta al archivo CSV de transacciones.")
    parser.add_argument(
        "--output-dir", default="output", help="Carpeta donde se guardarán los reportes."
    )
    return parser


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        result = run(args.input, args.output_dir)
    except ReportAutomationError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"Reporte generado: {result['excel_path']}")
    print(f"Reporte generado: {result['html_path']}")
    if result["skipped_rows"]:
        print(f"Filas omitidas por errores de datos: {result['skipped_rows']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
