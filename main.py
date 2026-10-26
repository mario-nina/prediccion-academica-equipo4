"""API mínima de predicción académica — Equipo 4."""
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

BASE = Path(__file__).resolve().parent
modelo = joblib.load(BASE / "modelo_equipo4.joblib")

app = FastAPI(
    title="Predicción del Rendimiento Académico — Equipo 4",
    description="Predicción simulada de nota final antes del examen final.",
    version="1.0",
)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


class DatosEstudiante(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    gestion: int = Field(ge=2023, le=2035)
    periodo: Literal["I", "II"]
    asignatura: Literal[
        "Programación I", "Programación II", "Bases de Datos",
        "Estructuras de Datos", "Ingeniería de Software",
    ]
    asistencia: float = Field(ge=0, le=100)
    horas_estudio: float = Field(ge=0, le=40)
    participacion_clase: float = Field(ge=0, le=10)
    promedio_anterior: float = Field(ge=0, le=100)
    porcentaje_entregas: float = Field(ge=0, le=100)
    puntualidad: float = Field(ge=0, le=100)
    entregable_1: float = Field(ge=0, le=100)
    entregable_2: float = Field(ge=0, le=100)
    entregable_3: float = Field(ge=0, le=100)
    entregable_4: float = Field(ge=0, le=100)


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(BASE / "static" / "index.html")


@app.post("/predecir", summary="Predecir la nota final")
def predecir(datos: DatosEstudiante):
    entrada = datos.model_dump()
    valores = (entrada["porcentaje_entregas"] + entrada["puntualidad"]) / 2
    continua = 0.225 * sum(entrada[f"entregable_{i}"] for i in range(1, 5)) + 0.10 * valores
    entrada["evaluacion_continua"] = round(continua, 2)

    prediccion = float(modelo.predict(pd.DataFrame([entrada]))[0])
    prediccion = min(100.0, max(0.0, prediccion))

    return {
        "evaluacion_continua": round(continua, 2),
        "nota_final_estimada": round(prediccion, 2),
    }
