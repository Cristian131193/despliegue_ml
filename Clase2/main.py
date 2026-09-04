from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

NOMBRE_BUNDLE = "modelo_bundle_e_cardiaca.pkl"

estado_servicio = {"bundle": None}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cargar el modelo al iniciar la aplicación
    estado_servicio["bundle"] = joblib.load(NOMBRE_BUNDLE)
    print(f"Modelo cargado desde {NOMBRE_BUNDLE}")
    yield
    # Aquí podrías agregar código para liberar recursos si es necesario al cerrar la aplicación
    estado_servicio["bundle"] = None

app = FastAPI(
    title="Predicción de Enfermedad Cardiaca", 
    description="API para predecir la presencia de enfermedad cardiaca en pacientes utilizando un modelo de machine learning entrenado.",   
    version="1.0.0",
    lifespan=lifespan
    )

class PacienteInput(BaseModel):
    sbp: int = Field(...,description="Presión arterial sistólica"),
    Tabaco: float = Field(...,description="Tabaco acumulado (kg)"),
    ldl: float = Field(...,description="Colesterol LDL"),
    Adiposidad: float = Field(...,description="Adiposidad"),
    Familia: Literal['Presente',
                     'Ausente'] = Field(
                         ...,description="Antecendentes familiares de enfermedad cardíaca"),
    Tipo: int = Field(...,description="Comportamiento tipo-A"),
    Obesidad: float = Field(...,description="Obesidad"),
    Alcohol:float = Field(...,description="Consumo actual de alcohol"),
    Edad:int = Field(...,description="Edad")


class PacienteOutput(BaseModel):
   chd_predicho: int
   probabilidad: float
   riesgo: str


@app.get("/" )
def estado():
    return {
        "estado": "API en funcionamiento",
        "modelo_cargado": estado_servicio["bundle"] is not None
    }


@app.post("/predecir", response_model=PacienteOutput)
def predecir(paciente: PacienteInput):
    #validar modelo
    bundle = estado_servicio["bundle"]
    if bundle is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    fila = paciente.model_dump()
    fila["Familia"] = bundle["mapeo_familia"][fila["Familia"]]
        
    X_nuevo = pd.DataFrame([fila])[bundle["columnas"]]
        
    prediccion = bundle["pipeline"].predict(X_nuevo)[0]
    probabilidad = bundle["pipeline"].predict_proba(X_nuevo)[0,1]

    #devolver resultados

    return PacienteOutput(
        chd_predicho=int(prediccion),
        probabilidad=round(float(probabilidad), 4),
        riesgo="Alto" if probabilidad > 0.5 else "Bajo"
    )

