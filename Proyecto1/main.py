from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import esquema

NOMBRE_BUNDLE = "modelo_churn.joblib"

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
    title="Predicción de cancelación de clientes", 
    description="API para predecir la cancelación de clientes utilizando un modelo de machine learning entrenado.",   
    version="1.0.0",
    lifespan=lifespan
    )


@app.get("/" )
def estado():
    return {
        "estado": "API en funcionamiento",
        "modelo_cargado": estado_servicio["bundle"] is not None
    }


@app.post("/predecir", response_model=esquema.RespuestaClasificacion)
def predecir(solicitud: esquema.SolicitudClasificacion):
    #validar modelo
    bundle = estado_servicio["bundle"]
    if bundle is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    
    fila = solicitud.model_dump()
        
    X_nuevo = pd.DataFrame([fila])[bundle["columnas"]]

    probabilidad = bundle["pipeline"].predict_proba(X_nuevo)[0,1]

    #devolver resultados

    return esquema.RespuestaClasificacion(
        probabilidad=round(float(probabilidad), 4),
        prediccion="Cancelación" if probabilidad > 0.5 else "No cancelación",
        riesgo="Alto" if probabilidad > 0.5 else "Bajo",
        umbral=0.5
    )

