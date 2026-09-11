#Construir la imagen del servicio

#La imagen base

FROM python:3.13-slim

#La carpeta donde va a vivir todo dentro del contenedor

WORKDIR /servicio

#Que los mensajes salgan

ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1

#Copiar los requerimientos
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]