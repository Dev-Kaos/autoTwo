"""  Dominio calculos puros no tienen idea de la existencia de algo de fuera, bases de datos o whats"""
# src/domain/logic.py
import pandas as pd


def formatear_tiempo_legible(td: pd.Timedelta) -> str:
    """Regla de negocio: Cómo queremos que el usuario vea el tiempo."""
    if pd.isnull(td):
        return "Sin datos"
    dias = td.days
    horas = td.components.hours
    minutos = td.components.minutes
    return f"{dias} días, {horas:02d}:{minutos:02d}"
