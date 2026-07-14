# Automatización de Reportes e Informes

Trabajo práctico experimental — Módulo **Automatización de Software**,
Maestría en Ingeniería en Software (UNEMI).

## Problemática

Generar reportes periódicos de ventas (resumen, ingresos por categoría y
top de productos) de forma manual es lento y propenso a errores. Este
proyecto automatiza el proceso: a partir de un archivo CSV de
transacciones, calcula los indicadores clave y genera automáticamente un
reporte en **Excel** y otro en **HTML**, listos para compartir.

## Estructura del proyecto

```
tarea_2/
├── .github/workflows/ci.yml     # Pipeline de integración continua
├── data/
│   └── sample_transactions.csv  # Datos de ejemplo
├── output/                      # Reportes generados (ignorado en git)
├── src/report_automation/
│   ├── __init__.py
│   ├── exceptions.py            # Excepciones propias del dominio
│   ├── data_loader.py           # Carga y validación del CSV de entrada
│   ├── processor.py             # Cálculo de KPIs (Equipo A)
│   ├── report_generator.py      # Generación de reportes Excel/HTML (Equipo B)
│   └── main.py                  # Punto de entrada (CLI)
├── tests/                       # Pruebas unitarias (Pytest)
├── ta2/                         # Enunciado de la actividad
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml               # Configuración de pytest y coverage
```

## Requisitos

- Python 3.11+

## Instalación (entorno virtual)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements-dev.txt
```

## Uso

```bash
python -m src.report_automation.main --input data/sample_transactions.csv --output-dir output
```

Esto genera `output/reporte_ventas.xlsx` y `output/reporte_ventas.html`
con el resumen de indicadores, el desglose por categoría y el top de
productos.

## Pruebas y cobertura

```bash
pytest --cov=src/report_automation --cov-report=term-missing --cov-report=html
```

El reporte de cobertura en HTML se genera en `htmlcov/index.html`.

## Estilo de código

```bash
flake8 src tests
```

## Flujo de ramas

| Rama        | Propósito                                              |
|-------------|---------------------------------------------------------|
| `main`      | Rama base del repositorio.                              |
| `developer` | Rama de trabajo activo del equipo (todo el desarrollo).|
| `staging`   | Versión validada, lista para despliegue.                |

Flujo de trabajo: desarrollar y probar en `developer` → push → esperar el
pipeline de GitHub Actions → corregir errores si los hay → una vez que
todas las pruebas pasen y el líder apruebe, integrar a `staging`.

## Integración continua

El workflow de GitHub Actions (`.github/workflows/ci.yml`) se ejecuta en
cada push/PR hacia `main`, `developer` y `staging`, y realiza:

1. Instalación de dependencias.
2. Análisis de estilo con `flake8`.
3. Ejecución de pruebas unitarias con `pytest`.
4. Generación y publicación del reporte de cobertura (HTML) como artefacto.

## Roles del equipo

| Rol                 | Integrante(s) | Aporte                                              |
|----------------------|---------------|------------------------------------------------------|
| Líder del proyecto    | _por definir_ | Configuración del repositorio, ramas y CI.           |
| Equipo A              | _por definir_ | `processor.py` — cálculo de KPIs.                    |
| Equipo B              | _por definir_ | `report_generator.py` — generación de reportes.      |
