from pydantic import BaseModel, Field

from datetime import date

class RegistroHistorico(BaseModel):
    fecha: date = Field(..., description="Fecha del registro histórico")
    unidades: int = Field(..., ge=0, description="Número de unidades vendidas en esa fecha")


class SolicitudPronostico(BaseModel):
    store: int = Field(ge=1,le=10, description="ID de la tienda del 1 al 10")
    item: int = Field(ge=1,le=50, description="ID del producto del 1 al 50")
    historial: list[RegistroHistorico] = Field(min_length=28, max_length=365, description="Lista de registros históricos de ventas")
    horizonte: int = Field(ge=1, le=28, description="Número de días para los cuales se desea el pronóstico")


