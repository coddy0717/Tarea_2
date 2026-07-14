"""Excepciones propias del paquete report_automation."""


class ReportAutomationError(Exception):
    """Excepción base de la aplicación."""


class DataLoadError(ReportAutomationError):
    """Error al leer o validar el archivo de datos de entrada."""


class ReportGenerationError(ReportAutomationError):
    """Error al generar un reporte de salida."""
