from pydantic import BaseModel, Field

class SolicitudClasificacion(BaseModel):
    antiguedad_meses: int = Field(..., ge=0, description="Antigüedad del cliente en meses")
    gasto_mensual: float = Field(..., ge=0, description="Gasto mensual del cliente")
    visitas_ultimo_mes: int = Field(..., ge=0, description="Número de visitas del cliente en el último mes")
    dias_desde_ultima_visita: int = Field(..., ge=0, description="Número de días desde la última visita del cliente")
    tickets_soporte: int = Field(..., ge=0, description="Número de tickets de soporte abiertos por el cliente")
    descuento_activo: int = Field(..., ge=0, le=1, description="Indica si el cliente tiene un descuento activo (0 o 1)")
    plan: str = Field(..., description="Plan del cliente (estandar, basico, premium)")
    metodo_pago: str = Field(..., description="Método de pago del cliente (tarjeta, transferencia, efectivo)")   

class RespuestaClasificacion(BaseModel):
   probabilidad: float
   prediccion: str
   riesgo: str
   umbral: float
