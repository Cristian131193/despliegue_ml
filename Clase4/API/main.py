from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
import Clase4.API.inferencia
import Clase4.API.esquema
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

NOMBRE_BUNDLE = "modelo_demanda.joblib"

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
    title="Predicción de Demanda", 
    description="API para predecir la demanda de productos utilizando un modelo de machine learning entrenado.",   
    version="1.0.0",
    lifespan=lifespan
    )

@app.get("/estado", summary="Estado del servicio", description="Verifica si el servicio " \
                                                        "está activo y el modelo cargado.")
async def estado():
    if estado_servicio["bundle"] is not None:
        return {"estado": "activo", "modelo_cargado": True}
    else:
        return {"estado": "inactivo", "modelo_cargado": False}

@app.post("/predecir", summary="Pronosticar demanda", description="Recibe un historial de ventas y devuelve " \
                                                        "las predicciones para los próximos días.")
def predecir(datos: Clase4.API.esquema.SolicitudPronostico):

    store = datos.store
    item = datos.item
    registros = datos.historial
    horizonte = datos.horizonte

    historial = pd.DataFrame(
        {
            "date": pd.to_datetime([r.fecha for r in registros]),
            "store": store,
            "item": item,
            "sales": [r.unidades for r in registros]

        }

    )

    bundle = estado_servicio["bundle"]

    pronostico = Clase4.API.inferencia.pronosticar(bundle, historial, horizonte)

    return {"store": store, "item": item, "pronostico": pronostico}





