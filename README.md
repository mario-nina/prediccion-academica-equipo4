# Predicción del Rendimiento Académico — Equipo 4

Aplicación mínima con FastAPI para estimar la nota final antes del examen final. Utiliza el modelo Ridge entrenado en el notebook del equipo, incluido en `modelo_equipo4.joblib`.

## Contenido

- `main.py`: API, validación de entradas y predicción.
- `modelo_equipo4.joblib`: modelo y preprocesamiento entrenados.
- `static/index.html`, `static/estilos.css`: interfaz web personalizable.
- `requirements.txt`: dependencias.
- `.python-version`: versión de Python para Render.

## Ejecutar localmente

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Abrir `http://127.0.0.1:8000` para usar el formulario y `http://127.0.0.1:8000/docs` para probar la API.

## Publicar en Render

1. Crear un repositorio en GitHub y subir el contenido de esta carpeta, incluida la carpeta `static` y el archivo `modelo_equipo4.joblib`.
2. En Render seleccionar `New > Web Service`, conectar el repositorio y escoger el plan gratuito si está disponible.
3. Configurar:
   - Language: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Abrir la URL de Render. La interfaz estará en `/` y la documentación de la API en `/docs`.

## Uso de la API

`POST /predecir` recibe JSON con los datos del estudiante. La evaluación continua se calcula de forma automática y **no** se solicita la nota del examen final.

La validación devuelve un error HTTP `422` si faltan campos, los rangos son inválidos o las categorías son desconocidas. La nota estimada se limita al intervalo 0–100.

## Notas

- Los datos usados para entrenar el modelo son sintéticos; la predicción no tiene validez institucional.
- Para mantener la misma versión del modelo no es necesario volver a entrenarlo en Render.
- El modelo `joblib` solo debe cargarse desde archivos de confianza.
- El modelo se entrenó con `scikit-learn==1.8.0`, lo que se conserva en `requirements.txt`.
